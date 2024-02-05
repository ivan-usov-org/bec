#!/usr/bin/env bash
# helper script to stop BEC server
set -e

CONDA_ENV=bec_env

module add psi-python39/2021.11

conda activate $CONDA_ENV
bec-server stop

echo "Stopping redis"
redis-cli shutdown
