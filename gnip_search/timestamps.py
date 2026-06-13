try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


MILLISECOND_UTC_SUFFIX = ".000Z"


def remove_millisecond_utc_suffix(value):
    """Remove only GNIP's exact millisecond UTC suffix from a timestamp."""
    if not isinstance(value, string_types) or not value:
        raise ValueError("GNIP posted time must be a non-empty string")
    if value.endswith(MILLISECOND_UTC_SUFFIX):
        timestamp = value[:-len(MILLISECOND_UTC_SUFFIX)]
        if not timestamp:
            raise ValueError("GNIP posted time must include a value before its suffix")
        return timestamp
    return value
