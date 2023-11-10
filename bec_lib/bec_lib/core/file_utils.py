import warnings

from bec_lib.file_utils import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.file_utils` is deprecated. Import from `bec_lib.file_utils` instead.",
    DeprecationWarning,
)
