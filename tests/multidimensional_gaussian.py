#!/usr/bin/env python
"""
Obtained from https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/core_examples/multidimensional_gaussian.py
Testing the recovery of a multi-dimensional
Gaussian with zero mean and unit variance
"""
from __future__ import division
import bilby
import numpy as np
import sys


# A few simple setup steps
label = sys.argv[1]
outdir = f'outdir_{label}'

# Generating simulated data: generating n-dim Gaussian

dim = 5
mean = np.zeros(dim)
cov = np.ones((dim, dim))
data = np.random.multivariate_normal(mean, cov, 100)


class MultidimGaussianLikelihood(bilby.Likelihood):
    """
        A multivariate Gaussian likelihood
        with known analytic solution.

        Parameters
        ----------
        data: array_like
            The data to analyse
        dim: int
            The number of dimensions
        """

    def __init__(self, data, dim):
        parmeters = {}
        for i in range(dim):
            parmeters[f"mu_{i}"] = None
            parmeters[f"sigma_{i}"] = None
        super().__init__(parameters=parmeters)
        self.dim = dim
        self.data = np.array(data)
        self.N = len(data)

    def log_likelihood(self):
        mu = np.array(
            [self.parameters["mu_{0}".format(i)] for i in range(self.dim)]
        )
        sigma = np.array(
            [self.parameters["sigma_{0}".format(i)] for i in range(self.dim)]
        )
        p = np.array([(self.data[n, :] - mu) / sigma for n in range(self.N)])
        return np.sum(
            -0.5 * (np.sum(p ** 2) + self.N * np.log(2 * np.pi * sigma ** 2))
        )


likelihood = MultidimGaussianLikelihood(data, dim)
priors = bilby.core.prior.PriorDict()
priors.update(
    {
        "mu_{0}".format(i): bilby.core.prior.Uniform(-5, 5, "mu")
        for i in range(dim)
    }
)
priors.update(
    {
        "sigma_{0}".format(i): bilby.core.prior.LogUniform(0.2, 5, "sigma")
        for i in range(dim)
    }
)
# And run sampler
# The plot arg produces trace_plots useful for diagnostics
result = bilby.run_sampler(
    likelihood=likelihood,
    priors=priors,
    sampler="dynesty",
    sample="rwalk_dynesty",
    npoints=500,
    walks=10,
    outdir=outdir,
    label=label,
    plot=True,
)
result.plot_corner()
