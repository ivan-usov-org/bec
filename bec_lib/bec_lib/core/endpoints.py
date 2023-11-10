import warnings

from bec_lib.endpoints import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.endpoints` is deprecated. Import from `bec_lib.endpoints` instead.",
    DeprecationWarning,
)
