import warnings

from bec_lib import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core` is deprecated. Import from `bec_lib` instead.",
    DeprecationWarning,
)
