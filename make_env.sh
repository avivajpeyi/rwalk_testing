conda create -n multipoint python=3.6 bilby_pipe gwpy
conda activate multipoint
pip uninstall dynesty
pip uninstall bilby

cd ..
git clone https://github.com/avivajpeyi/dynesty
cd dynesty
git checkout -b refactor_rwalk_to_return_more_points origin/refactor_rwalk_to_return_more_points
python setup.py develop

cd ..
git clone git@git.ligo.org:avi.vajpeyi/bilby.git
cd bilby
git checkout -b refactor_rwalk_to_return_more_points origin/refactor_rwalk_to_return_more_points
python setup.py develop
