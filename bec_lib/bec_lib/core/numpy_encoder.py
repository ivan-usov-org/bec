import warnings

from bec_lib.numpy_encoder import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.numpy_encoder` is deprecated. Import from `bec_lib.numpy_encoder` instead.",
    DeprecationWarning,
)
