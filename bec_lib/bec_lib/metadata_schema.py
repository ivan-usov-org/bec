from functools import cache

from pydantic import BaseModel, ConfigDict

from bec_lib import plugin_helper
from bec_lib.logger import bec_logger

logger = bec_logger.logger
_METADATA_SCHEMA_REGISTRY = {}


class BasicScanMetadata(BaseModel):
    """Scan metadata base class which behaves like a dict, and will accept any keys,
    like the existing metadata field in messages, but can be extended to add required
    fields for specific scans."""

    model_config = ConfigDict(extra="allow", validate_assignment=True)


@cache
def _get_metadata_schema_registry() -> dict[str, type[BasicScanMetadata]]:
    plugin_schema = plugin_helper.get_metadata_schema_registry()
    for name, schema in list(plugin_schema.items()):
        try:
            if not issubclass(schema, BasicScanMetadata):
                logger.warning(
                    f"Schema {schema} for {name} in the plugin registry is not valid! It must subclass BasicScanMetadata"
                )
                del plugin_schema[name]
        except TypeError:
            logger.warning(
                f"Schema {schema} for {name} in the plugin registry is not a valid type!"
            )
            del plugin_schema[name]
    return _METADATA_SCHEMA_REGISTRY | plugin_schema


def cache_clear():
    return _get_metadata_schema_registry.cache_clear()


def get_metadata_schema_for_scan(scan_name: str):
    """Return the pydantic model (must be a subclass of BasicScanMetadata)
    associated with the given scan. If none is found, returns BasicScanMetadata."""
    return _get_metadata_schema_registry().get(scan_name) or BasicScanMetadata
