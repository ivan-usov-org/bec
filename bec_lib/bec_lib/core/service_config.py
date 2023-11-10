import warnings

from bec_lib.service_config import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.service_config` is deprecated. Import from `bec_lib.service_config` instead.",
    DeprecationWarning,
)
