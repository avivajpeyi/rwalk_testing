import os

import pycondor

MULTI_RWALK = "multi_rwalk"
REGULAR_RWALK = "regular_rwalk"

EXE_ROOT = {
    MULTI_RWALK:
        "/home/avi.vajpeyi/.conda/envs/timeslides/bin",
    REGULAR_RWALK:
        "/cvmfs/oasis.opensciencegrid.org/ligo/sw/conda/envs/igwn-py38/bin"
}

PYTHON_PATHS = {
    MULTI_RWALK: f"{EXE_ROOT[MULTI_RWALK]}/python3",
    REGULAR_RWALK: f"{EXE_ROOT[REGULAR_RWALK]}/python3",
}

BILBY_PIPE_PATHS = {
    MULTI_RWALK: f"{EXE_ROOT[MULTI_RWALK]}/bilby_pipe",
    REGULAR_RWALK: f"{EXE_ROOT[REGULAR_RWALK]}/bilby_pipe",
}

BILBY_ANALYSIS_PATHS = {
    MULTI_RWALK: f"{EXE_ROOT[MULTI_RWALK]}/bilby_pipe_analysis",
    REGULAR_RWALK: f"{EXE_ROOT[REGULAR_RWALK]}/bilby_pipe_analysis",
}

TESTS = [
    'multidimensional_gaussian.py',
    '1d_guassian.py',
    'bns_injection.ini',
    'bbh_injection.ini',
    'fast_bbh_injection.ini',
]


def make_dag(rwalk_type):
    maindir = os.path.abspath(f"./jobsub_files")
    logdir = os.path.join(maindir, "log")
    subdir = os.path.join(maindir, "sub")
    dagman = pycondor.Dagman(name=rwalk_type, submit=subdir)
    for test_script in TESTS:
        test_type = os.path.basename(test_script).split(".")[1]
        basename = os.path.basename(test_script).split(".")[0]
        job_name = f"{rwalk_type}_{basename}"
        if test_type == "py":
            exe = PYTHON_PATHS[rwalk_type]
            args_str = f"{test_script} {job_name}"
        else:
            exe = BILBY_PIPE_PATHS[rwalk_type]
            analysis = BILBY_ANALYSIS_PATHS[rwalk_type]
            args_str = f"{test_script} "
            args_str += f"--label {job_name} "
            args_str += f"--outdir outdir_{job_name} "
            args_str += f"--analysis-executable {analysis} "
            args_str += f"--scheduler condor "
            args_str += f"--submit"

        job = pycondor.Job(
            name=job_name,
            executable=exe,
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
        job.add_arg(args_str)
    dagman.build_submit(submit_options="False", fancyname=False)
    print(
        f">>>\n condor_submit_dag {os.path.join(subdir, f'{rwalk_type}.submit')}\n>>>")


def main():
    make_dag(MULTI_RWALK)
    make_dag(REGULAR_RWALK)


if __name__ == "__main__":
    main()
