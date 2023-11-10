import warnings

from bec_lib.devicemanager import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.devicemanager` is deprecated. Import from `bec_lib.devicemanager` instead.",
    DeprecationWarning,
)
