import warnings

from bec_lib.tests.utils import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.tests.utils` is deprecated. Import from `bec_lib.tests.utils` instead.",
    DeprecationWarning,
)
