import os

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
    'gw150914.py'
]

SUB_FILE = """
universe = vanilla
executable = {EXE}

log = {LOGDIR}/{JOBNAME}.log
error = {LOGDIR}/{JOBNAME}.err
output = {LOGDIR}/{JOBNAME}.out

arguments = {ARGS_STRING}

getenv = True
accounting_group_user = avi.vajpeyi
accounting_group = ligo.dev.o3.cbc.pe.lalinference

notification = Always
request_memory = 3GB
request_disk = 500MB
priority=100

queue 1
"""


def make_condor_submission_files(rwalk_type):
    log_dir = f"{rwalk_type}_logs"
    os.makedirs(log_dir, exist_ok=True)
    for test_script in TESTS:
        basename = os.path.basename(test_script).split(".py")[0]
        job_name = f"{rwalk_type}_{basename}"
        sub_fname = f"{job_name}.submit"
        with open(sub_fname, "w") as f:
            f.write(SUB_FILE.format(
                EXE=PYTHON_PATHS[rwalk_type],
                LOGDIR=log_dir,
                ARGS_STRING=f"{test_script} {job_name}",
                JOBNAME=job_name
            ))
            print(f"condor_submit {sub_fname}")


def main():
    make_condor_submission_files(MULTI_RWALK)
    make_condor_submission_files(REGULAR_RWALK)


if __name__ == "__main__":
    main()
