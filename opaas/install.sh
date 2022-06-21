SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

pip install -r requirements.txt

pip install -e $SCRIPT_DIR/../bluekafka_utils

pip install -r $SCRIPT_DIR/../../ophyd_devices/requirements.txt
pip install -e $SCRIPT_DIR/../../ophyd_devices