import warnings

from bec_lib.pdf_writer import *

warnings.filterwarnings("default", category=DeprecationWarning)

warnings.warn(
    "Importing from `bec_lib.core.pdf_writer` is deprecated. Import from `bec_lib.pdf_writer` instead.",
    DeprecationWarning,
)
