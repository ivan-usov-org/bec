import logging

import bec_client_lib.core

from .device_serializer import is_serializable
from .devicemanager import rgetattr

loggers = logging.getLogger(__name__)
