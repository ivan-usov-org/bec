import warnings

from bec_lib.connector import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.connector` is deprecated. Import from `bec_lib.connector` instead.",
    DeprecationWarning,
)
