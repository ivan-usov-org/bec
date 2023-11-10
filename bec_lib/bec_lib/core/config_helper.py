import warnings

from bec_lib.config_helper import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.config_helper` is deprecated. Import from `bec_lib.config_helper` instead.",
    DeprecationWarning,
)
