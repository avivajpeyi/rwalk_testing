#!/usr/bin/env python
"""
Obtained from https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/core_examples/multidimensional_gaussian.py
Testing the recovery of a multi-dimensional
Gaussian with zero mean and unit variance
"""
from __future__ import division

import sys

import bilby
import numpy as np

np.random.seed(0)

DIM = 3
MU_RANGE = (-1, 1)
SIGMA_RANGE = (0.2, 5)


def get_multidim_gausian_prior():
    prior = {}
    for i in range(DIM):
        prior[f"mu_{i}"] = bilby.core.prior.Uniform(min(MU_RANGE), max(MU_RANGE), f"mu_{i}")
        prior[f"sigma_{i}"] = bilby.core.prior.Uniform(min(SIGMA_RANGE), max(SIGMA_RANGE), f"sigma_{i}")
    return bilby.core.prior.PriorDict(prior)


class MultidimGaussianLikelihood(bilby.Likelihood):

    def __init__(self, cov, mu):
        self.cov = np.atleast_2d(cov)
        self.mu = np.atleast_1d(mu)
        self.sigma = np.sqrt(np.diag(self.cov))
        self.N = 100
        self.data = np.random.multivariate_normal(mu, cov, 100)
        self.truths = {}
        parmeters = {}
        for i in range(DIM):
            parmeters[f"mu_{i}"] = None
            parmeters[f"sigma_{i}"] = None
            self.truths[f"mu_{i}"] = self.mu[i]
            self.truths[f"sigma_{i}"] = self.sigma[i]
        super().__init__(parameters=parmeters)

    def log_likelihood(self):
        mu = np.array([self.parameters["mu_{0}".format(i)] for i in range(DIM)])
        sigma = np.array([self.parameters["sigma_{0}".format(i)] for i in range(DIM)])
        p = np.array([(self.data[n, :] - mu) / sigma for n in range(self.N)])
        return np.sum(-0.5 * (np.sum(p ** 2) + self.N * np.log(2 * np.pi * sigma ** 2)))


def main():
    label = sys.argv[1]
    outdir = f'outdir_{label}'

    mean = np.zeros(DIM)
    sigma = np.ones(DIM)
    cov = np.zeros((DIM, DIM), int)
    np.fill_diagonal(cov, sigma)
    likelihood =MultidimGaussianLikelihood(cov=cov, mu=mean)
    result = bilby.run_sampler(
        likelihood=likelihood,
        priors=get_multidim_gausian_prior(),
        sampler="dynesty",
        sample="rwalk",
        npoints=1500,
        walks=100,
        outdir=outdir,
        label=label,
        plot=True,
    )
    result.plot_corner(truths=likelihood.truths)


if __name__ == "__main__":
    main()
