#!/usr/bin/env python
"""
https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/gw_examples/data_examples/GW150914.py

Tutorial to demonstrate running parameter estimation on GW150914

This example estimates all 15 parameters of the binary black hole system using
commonly used prior distributions. This will take several hours to run. The
data is obtained using gwpy, see [1] for information on how to access data on
the LIGO Data Grid instead.

[1] https://gwpy.github.io/docs/stable/timeseries/remote-access.html
"""
from __future__ import division, print_function

import os
import sys

import bilby
from gwpy.timeseries import TimeSeries

logger = bilby.core.utils.logger
label = sys.argv[1]
outdir = f'outdir_{label}'
bilby.core.utils.check_directory_exists_and_if_not_mkdir(outdir)

# Data set up
trigger_time = 1126259462

roll_off = 0.4  # Roll off duration of tukey window in seconds, default is 0.4s
duration = 4  # Analysis segment duration
post_trigger_duration = 2  # Time between trigger time and end of segment
end_time = trigger_time + post_trigger_duration
start_time = end_time - duration

psd_duration = 32 * duration
psd_start_time = start_time - psd_duration
psd_end_time = start_time

# We now use gwpy to obtain analysis and psd data and create the ifo_list
ifo_list = bilby.gw.detector.InterferometerList([])
for det in ["H1", "L1"]:

    ifo = bilby.gw.detector.get_empty_interferometer(det)

    data_file = os.path.join(outdir, f"{det}_data.hdf5")
    if os.path.exists(data_file):
        logger.info(f"Loading analysis data for ifo {det} from {data_file}")
        data = TimeSeries.read(data_file)
    else:
        logger.info(f"Downloading analysis data for ifo {det} from {data_file}")
        data = TimeSeries.fetch_open_data(det, start_time, end_time)
        data.write(data_file)
    ifo.strain_data.set_from_gwpy_timeseries(data)

    psd_file = os.path.join(outdir, f"{det}_psd.hdf5")
    if os.path.exists(psd_file):
        logger.info(f"Loading PSD data for ifo {det} from {psd_file}")
        psd_data = TimeSeries.read(psd_file)
    else:
        logger.info(f"Downloading PSD data for ifo {det} from {psd_file}")
        psd_data = TimeSeries.fetch_open_data(det, psd_start_time, psd_end_time)
        psd_data.write(data_file)

    psd_alpha = 2 * roll_off / duration
    psd = psd_data.psd(
        fftlength=duration,
        overlap=0,
        window=("tukey", psd_alpha),
        method="median"
    )
    ifo.power_spectral_density = bilby.gw.detector.PowerSpectralDensity(
        frequency_array=psd.frequencies.value, psd_array=psd.value)
    ifo_list.append(ifo)

logger.info("Saving data plots to {}".format(outdir))
ifo_list.plot_data(outdir=outdir, label=label)

priors = bilby.gw.prior.BBHPriorDict(filename='GW150914.prior')
waveform_generator = bilby.gw.WaveformGenerator(
    frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
    parameter_conversion=bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
    waveform_arguments={'waveform_approximant': 'IMRPhenomPv2',
                        'reference_frequency': 50})

# In this step, we define the likelihood. Here we use the standard likelihood
# function, passing it the data and the waveform generator.
likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
    ifo_list, waveform_generator, priors=priors, time_marginalization=True,
    phase_marginalization=True, distance_marginalization=True)

# Finally, we run the sampler. This function takes the likelihood and prior
# along with some options for how to do the sampling and how to save the data
result = bilby.run_sampler(
    likelihood, priors,
    sampler='dynesty',
    outdir=outdir,
    label=label,
    nact=10,
    nlive=1500,
    walks=100,
    n_check_point=10000,
    check_point_plot=True,
    sample="rwalk",
    conversion_function=bilby.gw.conversion.generate_all_bbh_parameters)
result.plot_corner()
