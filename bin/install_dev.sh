#!/usr/bin/env bash
# helper script to (re-)install BEC in a conda environment (in development mode)
set -e

CONDA_ENV=bec_env
PYTHON_VERSION="3.9"
BEC_DIR=bec_dev

module add psi-python39/2021.11

mkdir $BEC_DIR -p
cd $BEC_DIR || exit

echo "(Re-)creating conda environment: $CONDA_ENV"
conda create --name $CONDA_ENV python=$PYTHON_VERSION -y
conda activate $CONDA_ENV

echo "Installing dependencies"
conda install tmux -y
conda install redis-server -c conda-forge -y

echo "Cloning repositories"
for REPO in bec ophyd_devices
do
    if [ -d $REPO ]; then
        git -C $REPO pull
    else
        git clone https://gitlab.psi.ch/bec/$REPO.git
    fi
done

echo "Installing BEC"
pip install -e bec/bec_lib[dev]
pip install -e ophyd_devices[dev]
pip install -e bec/scan_server[dev]
pip install -e bec/scan_bundler[dev]
pip install -e bec/data_processing[dev]
pip install -e bec/file_writer[dev]
pip install -e bec/device_server[dev]
pip install -e bec/scihub[dev]
pip install -e bec/bec_client[dev]
pip install -e bec/bec_server[dev]
