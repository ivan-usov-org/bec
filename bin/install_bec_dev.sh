# helper script to (re-)install all BEC dependencies in freshly created virtual environment

# use getops to parse command line arguments; possible arguments are:
# -h: help
# -s: split virtual environment into separate environments for each package
# -c: conda environment name (default: bec_base_env)

# default values
split_env=false
conda_env_name="bec_base_env"

while getopts "hsc:" opt; do
    case ${opt} in
        h)
            echo "Usage: install_bec_dev.sh [-h] [-s] [-c <conda_env_name>]"
            echo "Options:"
            echo "-h: help"
            echo "-s: split virtual environment into separate environments for each package"
            echo "-c: conda environment name (default: bec_base_env)"
            exit 0
            ;;
        s)
            split_env=true
            ;;
        c)
            conda_env_name=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

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


# split virtual environment into separate environments for each package
if [ "$split_env" = true ]; then
    for package in "${dependencies[@]}"
    do
        echo "Creating virtual environment for $package..."
        conda activate ${conda_env_name}
        cd ./$package
        rm -rf ${package}_venv
        python -m venv ./${package}_venv
        conda deactivate
        source ./${package}_venv/bin/activate
        pip install -q -q -e .[dev]
        cd ../
        deactivate
        echo "Created virtual environment for $package"
    done
    source ./bec_server/bec_server_venv/bin/activate
    return
else # install all packages in one virtual environment
    echo "Creating single virtual environment for all packages..."
    conda activate ${conda_env_name}
    cd ./$package
    rm -rf ${package}_venv
    python -m venv ./${package}_venv
    conda deactivate    
    source ./${package}_venv/bin/activate
    pip install -q -q -e .[dev]
    cd ../
    echo "Created virtual environment for all packages"
fi




