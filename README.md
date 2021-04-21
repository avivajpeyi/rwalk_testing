# R-walk Tests

This repo documents various tests conducted to compare a new r-walk method that returns 
all the accepted points from it's random walks (normally > 100 walk steps).

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


<<<<<<< HEAD
## Changes:
- main changes are in Dynesty + Bilby.core.sampler.dynesty 
=======
## Changes
- Dynesty: https://github.com/avivajpeyi/dynesty/tree/refactor_rwalk_to_return_more_points
- Bilby: https://git.ligo.org/avi.vajpeyi/bilby/-/tree/refactor_rwalk_to_return_more_points
>>>>>>> d6ae9e4cad5de70847cc2a9d2b2eaa5935ca34cd

["fast_tutorial.py"]: https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/gw_examples/injection_examples/fast_tutorial.py
["multidimensional_gaussian.py"]: https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/core_examples/multidimensional_gaussian.py
["bns.py"]: https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/gw_examples/injection_examples/binary_neutron_star_example.py
["gw150914.py"]: https://git.ligo.org/lscsoft/bilby/-/blob/master/examples/gw_examples/data_examples/GW150914.py
[`ligo-igwn`]: https://computing.docs.ligo.org/conda/environments/igwn-py38/


---

## Notes from Rory:

I think I have a better way of explaining the example of returning points from the hypothetical list [0.1, 0.1, 0.2, 0.3, 0.3, 0.3, 0.04, 0.3, 0.1] btw!

Anyway, the key point is that we’re supposed to return genuine, honest random draws from the list [0.1, 0.1, 0.2, 0.3, 0.3, 0.3, 0.04, 0.3, 0.1]

So, there are 4 unique points. Let’s ask the following questions:
what’s the probability that I return [1,2,3,4] random points from that list. It’s 3/9*1/9*4/9*1/9~12/6000

So, is there a way to simulate that?

Well, I can pick each number from the list and say “i’ll accept it if I draw a uniform random number equal to or lower than it’s probability of appearing in the list”. In the limit that I do this an infinite number of times, this means that I accept this point exactly p(number) times. As a concrete example, say I pick 0.1, which has a probability of 3/9 of being accepted. If I accept it based on drawing a random number less than or equal to 3/9 then around 3/9th’s of the time I’ll accept it!

So I repeat that process for each number. On average, I accept each point with the right probability

And I accept exactly 1, 2, 3, or 4 points with the right probability: because the probability of accepting each point is independent

So you can scan through the list, pick a list-number, draw a random number and accept that point if the probability is less than or equal to that of the list-number

```
accept_step = int(act * ACCEPT_STEP_FACTOR)
act_accepted_us = u_list[::accept_step]
act_accepted_vs = v_list[::accept_step]
act_accepted_logls = logl_list[::accept_step]
act_num_accepted = len(act_accepted_us)
ncalls = [ncall] * act_num_accepted
blobs = [blob] * act_num_accepted

# create list for p(act_accepted_us)
# for each p(act_accepted_us) draw random num and see if I should keep the act_accepted_us
# unique_rows = np.unique(original_array, axis=0)

[array([0.60079568, 0.21111459]),
 array([0.55692637, 0.13981609]),
 array([0.39461896, 0.14885196]),
 array([0.43343924, 0.1764381 ]),
 array([0.39343211, 0.1559703 ]),
 array([0.50366912, 0.14008023]),
 array([0.47162877, 0.20864309]),
 array([0.67009312, 0.19454218]),
 array([0.63556565, 0.16720707]),
 array([0.51377984, 0.18588852])]

```