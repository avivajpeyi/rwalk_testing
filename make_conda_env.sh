export CONDA_ALWAYS_YES="true"
conda create -n multipoint python=3.6 gwpy bilby_pipe
conda activate multipoint
pip uninstall dynesty --yes
pip uninstall bilby --yes
cd ..
git clone https://github.com/avivajpeyi/dynesty dynesty_multipoint
cd dynesty_multipoint
git checkout -b refactor_rwalk_to_return_more_points origin/refactor_rwalk_to_return_more_points
python setup.py develop
cd ..
git clone git@git.ligo.org:avi.vajpeyi/bilby.git bilby_multipoint
cd bilby_multipoint
git checkout -b refactor_rwalk_to_return_more_points origin/refactor_rwalk_to_return_more_points
python setup.py develop
unset CONDA_ALWAYS_YES
