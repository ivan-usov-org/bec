from __future__ import annotations

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


_DEFAULT_SCHEMA = BasicScanMetadata


def _schema_is_ok(schema: type[BasicScanMetadata], name: str | None = None) -> bool:
    error_str = f"{'default' if name is None else ''} schema {schema} {('for scan '+name) if name else ''} is not valid!"
    try:
        if not issubclass(schema, BasicScanMetadata):
            logger.warning(f"{error_str} It must subclass BasicScanMetadata.")
            return False
    except TypeError:
        logger.warning(f"{error_str} It is not a valid type at all.")
        return False
    return True


@cache
def _get_metadata_schema_registry() -> dict[str, type[BasicScanMetadata]]:
    plugin_schema, default = plugin_helper.get_metadata_schema_registry()
    global _DEFAULT_SCHEMA
    _DEFAULT_SCHEMA = (
        default
        if (default is not None and _schema_is_ok(default, "default"))
        else BasicScanMetadata
    )
    for name, schema in list(plugin_schema.items()):
        if not _schema_is_ok(schema, name):
            del plugin_schema[name]
    return _METADATA_SCHEMA_REGISTRY | plugin_schema


def cache_clear():
    return _get_metadata_schema_registry.cache_clear()


def get_metadata_schema_for_scan(scan_name: str):
    """Return the pydantic model (must be a subclass of BasicScanMetadata)
    associated with the given scan. If none is found, returns BasicScanMetadata."""
    return _get_metadata_schema_registry().get(scan_name) or _DEFAULT_SCHEMA


def get_default_schema():
    return _DEFAULT_SCHEMA
