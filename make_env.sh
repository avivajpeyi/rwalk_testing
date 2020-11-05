conda create -n multipoint python=3.6 bilby bilby_pipe gwpy
conda activate multipoint
cd ..
git clone https://github.com/avivajpeyi/dynesty
cd dynesty
git checkout -b refactor_rwalk_to_return_more_points origin/refactor_rwalk_to_return_more_points
python setup.py install

