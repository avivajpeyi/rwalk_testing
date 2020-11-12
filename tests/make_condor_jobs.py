import os

import pycondor

MULTI_RWALK = "multi_rwalk"
REGULAR_RWALK = "regular_rwalk"

PYTHON_PATHS = {
    MULTI_RWALK:
        "/home/avi.vajpeyi/.conda/envs/timeslides/bin/python3",
    REGULAR_RWALK:
        "/cvmfs/oasis.opensciencegrid.org/ligo/sw/conda/envs/igwn-py38/bin/python3"
}

TESTS = [
    'multidimensional_gaussian.py',
    'bns.py',
    'fast_tutorial.py',
    'gw150914.py',
    '1d_guassian.py'
]


def make_dag(rwalk_type):
    maindir = os.path.abspath(f"./condor/{rwalk_type}")
    logdir = os.path.join(maindir, "log")
    subdir = os.path.join(maindir, "sub")
    dagman = pycondor.Dagman(name=rwalk_type, submit=subdir)
    for test_script in TESTS:
        basename = os.path.basename(test_script).split(".py")[0]
        job_name = f"{rwalk_type}_{basename}"
        job = pycondor.Job(
            name=job_name,
            executable=PYTHON_PATHS[rwalk_type],
            output=logdir,
            error=logdir,
            submit=subdir,
            request_memory="3GB",
            getenv="True",
            universe="vanilla",
            extra_lines=[
                "accounting_group_user = avi.vajpeyi",
                "accounting_group = ligo.dev.o3.cbc.pe.lalinference"
            ],
            dag=dagman
        )
        job.add_arg(f"{test_script} {job_name}")
    dagman.build_submit(submit_options="False", fancyname=False)
    print(f"condor_submit_dag {os.path.join(subdir, f'{rwalk_type}.submit')}")


def main():
    make_dag(MULTI_RWALK)
    make_dag(REGULAR_RWALK)


if __name__ == "__main__":
    main()
