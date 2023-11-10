import warnings

from bec_lib.bec_service import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.bec_service` is deprecated. Import from `bec_lib.bec_service` instead.",
    DeprecationWarning,
)
