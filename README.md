# R-walk Tests

This repo documents various tests conducted to compare a new r-walk method that returns all the accepted points from it's random walks (normally > 100 walk steps).

| Test                                      | Notes     |
|---                                        |---        |
| Non-GW ["multidimensional_gaussian.py"]   |           |
| Quick BBH injection ["fast_tutorial.py"]  |           |
| BNS injection ["bns.py"]                  |           |
| GW150914 ["gw150914.py"]                  |           |


## Steps to reproduce
1. Make envs
    - Make a conda env with the new rwalk methood (`bash make_env.sh`)
    - Make another conda env, this time using [`ligo-igwn`] settings
2. Run scripts in `tests` (in cmd/or as an HTC Condor job)
    - Run each of the scripts with the new rwalk env
    - Run each opf the scripts with the `ligo-igwn` env
    - For help with creation of HTC Condor job files use `tests/make_condor_jobs.py`


## Changes
- Dynesty: https://github.com/avivajpeyi/dynesty/tree/refactor_rwalk_to_return_more_points
- Bilby: https://git.ligo.org/avi.vajpeyi/bilby/-/tree/refactor_rwalk_to_return_more_points

["fast_tutorial.py"]: https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/gw_examples/injection_examples/fast_tutorial.py
["multidimensional_gaussian.py"]: https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/core_examples/multidimensional_gaussian.py
["bns.py"]: https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/gw_examples/injection_examples/binary_neutron_star_example.py
["gw150914.py"]: https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/gw_examples/data_examples/GW150914.py
[`ligo-igwn`]: https://computing.docs.ligo.org/conda/environments/igwn-py38/
