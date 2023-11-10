import warnings

from bec_lib.logbook_connector import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.logbook_connector` is deprecated. Import from `bec_lib.logbook_connector` instead.",
    DeprecationWarning,
)
