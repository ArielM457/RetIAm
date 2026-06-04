from collections.abc import Mapping


def read_field(source: object, key: str, default=None):
    if isinstance(source, Mapping):
        return source.get(key, default)
    return getattr(source, key, default)


def response_data(response, default=None):
    data = getattr(response, "data", None)
    if data is None:
        return default
    return data
