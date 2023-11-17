# pylint: skip-file
from bec_lib.tests.utils import bec_client


def test_nested_device_root(bec_client):
    dev = bec_client.device_manager.devices
    assert dev.dyn_signals.name == "dyn_signals"
    assert dev.dyn_signals.messages.name == "messages"
    assert dev.dyn_signals.root == dev.dyn_signals
    assert dev.dyn_signals.messages.root == dev.dyn_signals
