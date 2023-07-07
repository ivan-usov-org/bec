# helper script to (re-)install all BEC dependencies in freshly created virtual environment

conda_env_name="bec_base_env"

# check if conda is installed
if ! [ "$(which conda)" ]; then
    echo "conda is not installed. Please install conda first."
    return
fi

# check if conda environment exists and install it if not
if ! conda env list | grep -q ${conda_env_name}; then
    echo "Creating conda environment ${conda_env_name}..."
    conda create --name ${conda_env_name} python=3.8 redis
fi

for i in $(seq ${CONDA_SHLVL}); do
    conda deactivate
done

dependencies=(bec_lib scan_server scan_bundler data_processing file_writer device_server scihub bec_client bec_server)

# loop over all packages and install them
for package in "${dependencies[@]}"
do
    echo "Installing $package..."
    conda activate ${conda_env_name}
    cd ./$package
    rm -rf ${package}_venv
    python -m venv ./${package}_venv
    conda deactivate    
    source ./${package}_venv/bin/activate
    pip install -q -q -e .
    cd ../
    deactivate
    echo "Installed $package"
done

source ./bec_server/bec_server_venv/bin/activate


