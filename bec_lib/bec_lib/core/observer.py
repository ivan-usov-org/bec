import warnings

from bec_lib.observer import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.observer` is deprecated. Import from `bec_lib.observer` instead.",
    DeprecationWarning,
)
