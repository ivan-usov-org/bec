import warnings

from bec_lib.bec_errors import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.bec_errors` is deprecated. Import from `bec_lib.bec_errors` instead.",
    DeprecationWarning,
)
