import json

from ophyd import Device, PositionerBase, Signal


def is_serializable(f) -> bool:
    try:
        json.dumps(f)
        return True
    except (TypeError, OverflowError):
        return False


def get_custom_user_access_info(obj, obj_interface):

    # user_funcs = get_user_functions(obj)
    if hasattr(obj, "USER_ACCESS"):
        for f in [f for f in dir(obj) if f in obj.USER_ACCESS]:
            if f == "controller" or f == "on":
                print(f)
            m = getattr(obj, f)
            if not callable(m):
                if is_serializable(m):
                    obj_interface[f] = {"type": type(m).__name__}
                elif get_device_base_class(m) == "unknown":
                    obj_interface[f] = get_custom_user_access_info(m, {})
                else:
                    continue
            else:
                obj_interface[f] = {"type": "func", "doc": m.__doc__}
    return obj_interface


def get_device_base_class(obj) -> str:
    if isinstance(obj, PositionerBase):
        return "positioner"
    elif isinstance(obj, Signal):
        return "signal"
    elif isinstance(obj, Device):
        return "device"
    else:
        return "unknown"


def get_device_info(obj, device_info):
    """
    {
        "device_name": "samx",
            "device_info": {
                "device_base_class": "",
                "signals": {},
                "custom_user_access": {},
                "sub_devices": {
                    "device_name": "samx_sub",
                    "device_info": {
                        "device_base_class": "",
                        "signals": {},
                        "custom_user_access": {},
                        "sub_devices": {},
                    },
                },
            },
        }

    Args:
        obj (_type_): _description_
        device_info (_type_): _description_

    Returns:
        _type_: _description_
    """
    user_access = get_custom_user_access_info(obj, {})
    signals = []
    if hasattr(obj, "component_names"):
        for component_name in obj.component_names:
            if get_device_base_class(getattr(obj, component_name)) == "signal":
                signals.append(component_name)
    sub_devices = []
    if hasattr(obj, "walk_subdevices"):
        for name, dev in obj.walk_subdevices():
            sub_devices.append(get_device_info(dev, {}))
    return {
        "device_name": obj.name,
        "device_info": {
            "device_base_class": get_device_base_class(obj),
            "signals": signals,
            "sub_devices": sub_devices,
            "custom_user_access": user_access,
        },
    }
