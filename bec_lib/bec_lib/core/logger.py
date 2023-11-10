import warnings

from bec_lib.logger import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.logger` is deprecated. Import from `bec_lib.logger` instead.",
    DeprecationWarning,
)
