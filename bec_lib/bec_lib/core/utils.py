import warnings

from bec_lib.utils import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.utils` is deprecated. Import from `bec_lib.utils` instead.",
    DeprecationWarning,
)
