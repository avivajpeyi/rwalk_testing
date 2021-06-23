mkdir -p rwalk_files/
cd rwalk_files
mkdir -p envs
mkdir -p packages/main
mkdir -p packages/modded

echo "creating venv with main/master branch of software"
python3 -m venv envs/main && source envs/main/bin/activate
git clone https://github.com/joshspeagle/dynesty.git packages/main/dynesty_main
cd packages/main/dynesty_main && python setup.py develop && cd -
git clone git@git.ligo.org:lscsoft/bilby.git packages/main/bilby_main
cd packages/main/bilby_main && pip install -r requirements.txt && python setup.py develop && pip install bilby_pipe && cd -
deactivate

echo "creating venv with modded branch of software"
python3 -m venv envs/modded && source envs/modded/bin/activate
git clone https://github.com/avivajpeyi/dynesty packages/modded/dynesty_modded
cd packages/modded/dynesty_modded && git checkout -b refactor_rwalk_to_return_more_points origin/refactor_rwalk_to_return_more_points && python setup.py develop && cd -
git clone git@git.ligo.org:avi.vajpeyi/bilby.git packages/modded/bilby_modded
cd  packages/modded/bilby_modded && pip install -r requirements.txt && git checkout -b refactor_rwalk_to_return_more_points origin/refactor_rwalk_to_return_more_points && python setup.py develop && pip install bilby_pipe && cd -
deactivate 
