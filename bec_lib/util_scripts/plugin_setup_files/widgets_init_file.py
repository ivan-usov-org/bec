"""Module for user-created widget files and some utilities to load them."""

import inspect
import pkgutil
from importlib import util as importlib_util
from importlib.machinery import FileFinder, SourceFileLoader
from types import ModuleType

from bec_widgets import BECWidget
from my_plugin_repo.bec_widgets import widgets


def get_all_plugin_widgets() -> dict[str, BECWidget]:
    """BEC uses this function to load widgets from this plugin repository. Don't modify it unless
    you are absolutely certain of what you are doing!"""
    return _all_widgets_from_all_submodules(widgets)


def _get_widgets_from_module(module: ModuleType) -> dict[str, BECWidget]:
    """Find any BECWidget subclasses in the given module and return them with their names."""
    return dict(
        inspect.getmembers(
            module,
            predicate=lambda item: inspect.isclass(item)
            and issubclass(item, BECWidget)
            and item is not BECWidget,
        )
    )


def _all_widgets_from_all_submodules(module):
    """Recursively load submodules, find any BECWidgets, and return them all as a flat dict."""
    widgets = _get_widgets_from_module(module)
    if not hasattr(module, "__path__"):
        return widgets
    submodule_specs = (
        module_info.module_finder.find_spec(module_info.name)
        for module_info in pkgutil.iter_modules(module.__path__)
        if isinstance(module_info.module_finder, FileFinder)
    )
    for submodule in (
        importlib_util.module_from_spec(spec) for spec in submodule_specs if spec is not None
    ):
        assert isinstance(
            submodule.__loader__, SourceFileLoader
        ), "Module found from FileFinder should have SourceFileLoader!"
        submodule.__loader__.exec_module(submodule)
        widgets.update(_all_widgets_from_all_submodules(submodule))
    return widgets


if __name__ == "__main__":  # pragma: no cover
    print(get_all_plugin_widgets())
