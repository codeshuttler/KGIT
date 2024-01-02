pushd kgit
conda create --prefix=kgitenv python=3.8.13 --yes
eval "$(conda shell.bash hook)"
conda init
conda activate ./kgitenv
pip install -r requirements.txt
popd