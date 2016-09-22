#!/bin/sh

python -m venv --upgrade myvenv
myvenv/Scripts/activate.bat

pip install --upgrade 'pandas~=0.18.0'
pip install --upgrade 'matplotlib~=1.5.1'

source ./run.sh

myvenv/Scripts/deactivate.bat
