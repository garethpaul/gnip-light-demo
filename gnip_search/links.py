import ast


MAX_SERIALIZED_LINK_CHARS = 65536
MAX_LINK_VALUES = 1000
MAX_LINK_CHARS = 4096


try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


class LinkParseError(ValueError):
    pass


def parse_link_values(serialized):
    if not isinstance(serialized, string_types) or not serialized.strip():
        raise LinkParseError("GNIP link data must be a nonblank string")
    if len(serialized) > MAX_SERIALIZED_LINK_CHARS:
        raise LinkParseError("GNIP link data exceeds the size limit")

    try:
        parsed = ast.literal_eval(serialized)
    except (SyntaxError, ValueError, TypeError, MemoryError, RuntimeError):
        raise LinkParseError("GNIP link data is not a valid literal")

    if isinstance(parsed, string_types):
        values = [parsed]
    elif isinstance(parsed, (list, tuple, set)):
        values = list(parsed)
    else:
        raise LinkParseError("GNIP link data must contain a string collection")

    if not values or len(values) > MAX_LINK_VALUES or any(
            not isinstance(value, string_types) or not value.strip() or
            len(value) > MAX_LINK_CHARS
            for value in values):
        raise LinkParseError("GNIP link values exceed the accepted boundaries")

    return values
