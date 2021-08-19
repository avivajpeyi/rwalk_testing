from __future__ import division, print_function

import sys

import bilby
import numpy as np

np.random.seed(0)

MU_RANGE = (-1, 1)
SIGMA_RANGE = (0.2, 5)


def get_gaussian_prior():
    return bilby.core.prior.PriorDict({
        "mu": bilby.core.prior.Uniform(*MU_RANGE),
        "sigma": bilby.core.prior.Uniform(*SIGMA_RANGE)
    })


class SimpleGaussianLikelihood(bilby.Likelihood):
    def __init__(self, data):
        super().__init__(parameters={'mu': None, 'sigma': None})
        self.data = data
        self.N = len(data)

    def log_likelihood(self):
        mu = self.parameters['mu']
        sigma = self.parameters['sigma']
        res = self.data - mu
        return -0.5 * (np.sum((res / sigma) ** 2) + self.N * np.log(
            2 * np.pi * sigma ** 2))

    def analytical_log_likelihood(self, priors):
        """Z = int dmu_i dsig_i * likelihood(mi_i, sig_i,) * prior(mi_i, sig_i,)"""
        n = 1000
        mu_vals = np.linspace(*MU_RANGE, num=n)
        sig_vals = np.linspace(*SIGMA_RANGE, num=n)
        z = 0
        dm, ds = mu_vals[1] - mu_vals[0], sig_vals[1] - sig_vals[0]
        for mu, sig in zip(mu_vals, sig_vals):
            self.parameters.update(dict(mu=mu, sigma=sig))
            l = np.exp(self.log_likelihood())
            z += l * priors.prob(self.parameters) * dm * ds
        return np.log(z)


def main():
    if len(sys.argv) > 1:
        label = sys.argv[1]
    else:
        label = "simple"
    outdir = f'outdir_{label}'
    mean, sigma = 0, 1
    data = np.random.normal(mean, sigma, 100)
    gaussian_priors = get_gaussian_prior()
    likelihood = SimpleGaussianLikelihood(data=data)

    result = bilby.run_sampler(
        likelihood=likelihood,
        priors=gaussian_priors,
        sampler="dynesty",
        sample="rwalk",
        npoints=1500,
        walks=100,
        nact=1,
        outdir=outdir,
        label=label,
        plot=True,
        clean=True,
        dlogz=0.1
    )
    result.plot_corner(truths=dict(mu=mean, sigma=sigma))

    print(f"Estimated Evid: {result.log_evidence}")
    print(f"Analytical Evid: {likelihood.analytical_log_likelihood(gaussian_priors)}")


if __name__ == "__main__":
    main()
