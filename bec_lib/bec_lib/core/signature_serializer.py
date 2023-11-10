import warnings

from bec_lib.signature_serializer import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.signature_serializer` is deprecated. Import from `bec_lib.signature_serializer` instead.",
    DeprecationWarning,
)
