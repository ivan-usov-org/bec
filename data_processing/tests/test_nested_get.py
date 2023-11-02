from data_processing.stream_processor import nested_get


def test_nested_get_default():
    """
    Test the nested_get function.
    """
    data = {"a": {"b": {"c": 1}}}
    assert nested_get(data, "a.b.c") == 1


def test_nested_get_returns_default():
    """
    Test the nested_get function.
    """
    data = {"a": {"b": {"c": 1}}}
    assert nested_get(data, "a.b.d", 2) == 2


def test_nested_get_with_plain_key():
    """
    Test the nested_get function.
    """
    data = {"a": {"b": 1}}
    assert nested_get(data, "a") == {"b": 1}


def test_nested_get_with_missing_key():
    """
    Test the nested_get function.
    """
    data = {"a": {"b": 1}}
    assert nested_get(data, "c") == None
