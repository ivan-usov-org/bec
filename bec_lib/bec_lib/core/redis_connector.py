import warnings

from bec_lib.redis_connector import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.redis_connector` is deprecated. Import from `bec_lib.redis_connector` instead.",
    DeprecationWarning,
)
