#!/usr/bin/env bash
# helper script to start BEC server
set -e

CONDA_ENV=bec_env

module add psi-python39/2021.11

conda activate $CONDA_ENV
echo "Starting redis"
redis-server --daemonize yes

echo "Starting BEC server"
python ./bec/bec_lib/util_scripts/init_config.py --config ./bec/bec_lib/bec_lib/configs/demo_config.yaml
bec-server start --config ./bec/ci/test_config.yaml
