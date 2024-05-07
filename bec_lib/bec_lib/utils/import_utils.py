import sys
from importlib import import_module

from bec_lib.utils.proxy import Proxy


def lazy_import(module_name):
    return Proxy(lambda: import_module(module_name), init_once=True)


def lazy_import_from(module_name, from_list):
    ret = (Proxy(lambda: getattr(import_module(module_name), name)) for name in from_list)
    if len(from_list) == 1:
        return next(ret)
    else:
        return ret
