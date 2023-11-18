import builtins
import inspect
from typing import Any, Callable, List, Literal


def serialize_dtype(dtype: type) -> Any:
    """
    Convert a dtype to a string.

    Args:
        dtype (type): Data type

    Returns:
        str: String representation of the data type
    """
    if hasattr(dtype, "__name__"):
        name = dtype.__name__
        # changed in python 3.10. Refactor this when we upgrade
        if name != "Literal":
            return name
    if hasattr(dtype, "__module__"):
        if dtype.__module__ == "typing":
            return {"Literal": dtype.__args__}
    raise ValueError(f"Unknown dtype {dtype}")


def deserialize_dtype(dtype: Any) -> type:
    """
    Convert a serialized dtype to a type.

    Args:
        dtype (str): String representation of the data type

    Returns:
        type: Data type
    """
    if dtype == "_empty":
        # pylint: disable=protected-access
        return inspect._empty
    if isinstance(dtype, dict):
        # bodge needed for python 3.8
        if "Literal" in dtype:
            literal = Literal["dummy"]
            literal.__args__ = dtype["Literal"]
            return literal
        raise ValueError(f"Unknown dtype {dtype}")
    return builtins.__dict__.get(dtype)


def signature_to_dict(func: Callable, include_class_obj=False) -> dict:
    """
    Convert a function signature to a dictionary.
    The dictionary can be used to reconstruct the signature using dict_to_signature.

    Args:
        func (Callable): Function to be converted

    Returns:
        dict: Dictionary representation of the function signature
    """
    out = []
    params = inspect.signature(func).parameters
    for param_name, param in params.items():
        if not include_class_obj and param_name == "self" or param_name == "cls":
            continue
        # pylint: disable=protected-access
        out.append(
            {
                "name": param_name,
                "kind": param.kind.name,
                "default": param.default if param.default != inspect._empty else "_empty",
                "annotation": serialize_dtype(param.annotation),
            }
        )
    return out


def dict_to_signature(params: List[dict]) -> inspect.Signature:
    """
    Convert a dictionary representation of a function signature to a signature object.

    Args:
        params (List[dict]): List of dictionaries representing the function signature

    Returns:
        inspect.Signature: Signature object
    """
    out = []
    for param in params:
        # pylint: disable=protected-access
        out.append(
            inspect.Parameter(
                name=param["name"],
                kind=getattr(inspect.Parameter, param["kind"]),
                default=param["default"] if param["default"] != "_empty" else inspect._empty,
                annotation=deserialize_dtype(param["annotation"]),
            )
        )
    return inspect.Signature(out)
