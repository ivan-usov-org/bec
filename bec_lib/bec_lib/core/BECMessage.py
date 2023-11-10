import warnings

from bec_lib.messages import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.BECMessage` is deprecated. Import from `bec_lib.messages` instead.",
    DeprecationWarning,
)
