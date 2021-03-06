import functools
import glob

import bilby
import corner
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np

CORNER_KWARGS = dict(
    smooth=0.9,
    label_kwargs=dict(fontsize=16),
    title_kwargs=dict(fontsize=16),
    quantiles=[0.16, 0.84],
    levels=(1 - np.exp(-0.5), 1 - np.exp(-2), 1 - np.exp(-9 / 2.)),
    plot_density=False,
    plot_datapoints=False,
    fill_contours=True,
    show_titles=False,
    max_n_ticks=3,
    title_fmt=".2E",
)

from typing import List, Optional
import seaborn as sns


def get_colors(num_colors: int, alpha: Optional[float] = 1) -> List[List[float]]:
    """Get a list of colorblind colors,
    :param num_colors: Number of colors.
    :param alpha: The transparency
    :return: List of colors. Each color is a list of [r, g, b, alpha].
    """
    cs = sns.color_palette(palette="colorblind", n_colors=num_colors)
    cs = [list(c) for c in cs]
    for i in range(len(cs)):
        cs[i].append(alpha)
    return cs


def overlaid_corner(samples_list, sample_labels, param=[], truths=None,
                    fname="test.png"):
    """Plots multiple corners on top of each other"""
    print(f"Creating {fname}")
    n = len(samples_list)

    max_len = max([len(s) for s in samples_list])
    colors = get_colors(len(samples_list) + 1)

    joined_samples = pd.concat(samples_list)
    plot_range = [(min(joined_samples[p]), max(joined_samples[p])) for p in param]

    fig = corner.corner(
        samples_list[0],
        color=colors[0],
        truths=truths,
        range=plot_range,
        truth_color=colors[-1],
        hist_kwargs=dict(density=True, color=colors[0]),
        **CORNER_KWARGS
    )

    for idx in range(1, n):
        fig = corner.corner(
            samples_list[idx],
            fig=fig,
            range=plot_range,
            weights=get_normalisation_weight(len(samples_list[idx]), max_len),
            color=colors[idx],
            hist_kwargs=dict(density=True, color=colors[idx]),
            **CORNER_KWARGS
        )

    plt.legend(
        handles=[
            mlines.Line2D([], [], color=colors[i], label=sample_labels[i])
            for i in range(n)
        ],
        fontsize=20, frameon=False,
        bbox_to_anchor=(1, n), loc="upper right"
    )
    plt.savefig(fname)
    plt.close()

def get_normalisation_weight(len_current_samples, len_of_longest_samples):
    return np.ones(len_current_samples) * (len_of_longest_samples / len_current_samples)


def exception(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print(f"There was an exception in {function.__name__}: {e}")

    return wrapper


RES = {
    'multidimensional_gaussian.py': [
        '../tests/outdir_regular_rwalk_multidimensional_gaussian/regular_rwalk_multidimensional_gaussian_result.json',
        '../tests/outdir_multi_rwalk_multidimensional_gaussian/multi_rwalk_multidimensional_gaussian_result.json',
    ],
    'bns.py': [
        '../tests/outdir_regular_rwalk_bns/regular_rwalk_bns_result.json',
        '../tests/outdir_multi_rwalk_bns/multi_rwalk_bns_result.json'
    ],
    'fast_tutorial.py': [
        '../tests/outdir_regular_rwalk_fast_bbh_injection/result/regular_rwalk_fast_bbh_injection_data0_0-0_analysis_H1_dynesty_result.json',
        '../tests/outdir_multi_rwalk_fast_bbh_injection/result/multi_rwalk_fast_bbh_injection_data0_0-0_analysis_H1_dynesty_result.json'
    ],
    'bbh.py': [
        '../tests/outdir_regular_rwalk_bbh_injection/result/regular_rwalk_bbh_injection_data0_0-0_analysis_H1L1V1_dynesty_result.json',
        '../tests/outdir_multi_rwalk_bbh_injection/result/multi_rwalk_bbh_injection_data0_0-0_analysis_H1L1V1_dynesty_result.json'
    ],
    'gw150914.py': [
        '../tests/outdir_regular_rwalk_GW150914/result/regular_rwalk_GW150914_data0_1126259462-4_analysis_H1L1_dynesty_merge_result.json',
        '../tests/outdir_multi_rwalk_GW150914/result/multi_rwalk_GW150914_data0_1126259462-4_analysis_H1L1_dynesty_merge_result.json'
    ],
    '1d_gaussian.py': [
        "../tests/outdir_regular_rwalk_1d_guassian/regular_rwalk_1d_guassian_result.json",
        "../tests/outdir_multi_rwalk_1d_guassian/multi_rwalk_1d_guassian_result.json",
    ]
}


def get_result_paths():
    TESTS = [
        'multidimensional_gaussian.py',
        'bns.py',
        'fast_tutorial.py',
        'gw150914.py'
    ]
    results = glob.glob("tests/out*/*result.json")

    test_result = {k: [] for k in TESTS}
    for t in TESTS:
        for r in results:
            if t in r:
                test_result[t].append(r)
    return test_result


def print_info(normal, multi, fname):
    with open(fname, "w") as f:
        f.write(f"Normal:\n{(normal.sampling_time) / (60 * 60):.2f}hr\n{normal}")
        f.write(f"Multi:\n{(multi.sampling_time) / (60 * 60):.2f}hr\n{multi}")


@exception
def oned_gauss():
    r = RES["1d_gaussian.py"]
    normal = bilby.gw.result.CBCResult.from_json(r[0])
    multi = bilby.gw.result.CBCResult.from_json(r[1])
    samples_list = [normal.posterior, multi.posterior]
    param = [f"mu", "sigma", "log_likelihood"]
    overlaid_corner(
        samples_list=[s[param] for s in samples_list],
        sample_labels=["normal", "multi"],
        fname="1d_corner.png",
        truths=[0, 1, None]
    )
    print_info(normal, multi, "1d_stats.txt")


@exception
def multid():
    dim = 3
    mean = np.zeros(dim)
    cov = np.zeros((dim, dim), int)
    np.fill_diagonal(cov, 1)
    sigma = np.sqrt(np.diag(cov))
    r = RES["multidimensional_gaussian.py"]
    normal = bilby.gw.result.CBCResult.from_json(r[0])
    multi = bilby.gw.result.CBCResult.from_json(r[1])
    samples_list = [normal.posterior, multi.posterior]
    param = [f"mu_{i}" for i in range(dim)] + [f"sigma_{i}" for i in range(dim)] + [
        "log_likelihood"]
    truths = list(np.concatenate((mean, sigma, [None]), axis=None))
    overlaid_corner(
        samples_list=[s[param] for s in samples_list],
        sample_labels=["normal", "multi"],
        fname="multidim_corner.png",
        truths=truths
    )
    print_info(normal, multi, "multidim_stats.txt")


def fast_tut():
    r = RES["fast_tutorial.py"]
    normal = bilby.gw.result.CBCResult.from_json(r[0])
    multi = bilby.gw.result.CBCResult.from_json(r[1])
    samples_list = [normal.posterior, multi.posterior]
    param = ['mass_ratio', 'chirp_mass', 'luminosity_distance', 'theta_jn'] + [
        "log_likelihood"]
    truths = bilby.gw.conversion.generate_all_bbh_parameters(
        normal.injection_parameters)
    truths = [truths.get(p, None) for p in param]
    overlaid_corner(
        samples_list=[s[param] for s in samples_list],
        sample_labels=["normal", "multi"],
        fname="fast_corner.png",
        truths=truths
    )
    print_info(normal, multi, "fast_stats.txt")

def bbh():
    r = RES["bbh.py"]
    normal = bilby.gw.result.CBCResult.from_json(r[0])
    multi = bilby.gw.result.CBCResult.from_json(r[1])
    samples_list = [normal.posterior, multi.posterior]
    param = ["mass_ratio",
             "chirp_mass",
             "mass_1",
             "mass_2",
             "a_1",
             "a_2",
             "tilt_1",
             "tilt_2",
             "phi_12",
             "phi_jl",
             "luminosity_distance",
             "dec",
             "ra",
             "theta_jn",
             "psi",
             "phase",
             "geocent_time"] + ["log_likelihood"]
    truths = bilby.gw.conversion.generate_all_bbh_parameters(
        normal.injection_parameters)
    truths = [truths.get(p, None) for p in param]
    overlaid_corner(
        samples_list=[s[param] for s in samples_list],
        sample_labels=["normal", "multi"],
        fname="bbh_corner.png",
        truths=truths
    )
    print_info(normal, multi, "bbh.txt")



@exception
def gw150914():
    r = RES["gw150914.py"]
    normal = bilby.gw.result.CBCResult.from_json(r[0])
    multi = bilby.gw.result.CBCResult.from_json(r[1])
    samples_list = [normal.posterior, multi.posterior]
    param = ["mass_ratio",
             "chirp_mass",
             "mass_1",
             "mass_2",
             "a_1",
             "a_2",
             "tilt_1",
             "tilt_2",
             "phi_12",
             "phi_jl",
             "luminosity_distance",
             "dec",
             "ra",
             "theta_jn",
             "psi",
             "phase",
             "geocent_time"] + ["log_likelihood"]
    overlaid_corner(
        samples_list=[s[param] for s in samples_list],
        sample_labels=["normal", "multi"],
        fname="gw150914_corner.png"
    )
    print_info(normal, multi, "gw150914_stats.txt")


@exception
def bns():
    r = RES["bns.py"]
    normal = bilby.gw.result.CBCResult.from_json(r[0])
    multi = bilby.gw.result.CBCResult.from_json(r[1])
    samples_list = [normal.posterior, multi.posterior]
    param = ["chirp_mass", "symmetric_mass_ratio", "lambda_tilde", "delta_lambda"] + [
        "log_likelihood"]
    truths = bilby.gw.conversion.generate_all_bns_parameters(
        normal.injection_parameters)
    truths = [truths.get(p, None) for p in param]
    overlaid_corner(
        samples_list=[s[param] for s in samples_list],
        sample_labels=["normal", "multi"],
        fname="bns_corner.png",
        truths=truths
    )
    print_info(normal, multi, "bns_stats.txt")


def main():
    fast_tut()
    bns()
    bbh()
    gw150914()
    multid()
    oned_gauss()


if __name__ == "__main__":
    main()
