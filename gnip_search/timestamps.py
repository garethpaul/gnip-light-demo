import datetime
import re


try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


UTC_TIMESTAMP_RE = re.compile(
    r"^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2})(?:\.([0-9]{1,6}))?Z$")


def remove_millisecond_utc_suffix(value):
    """Validate a GNIP UTC timestamp and return whole-second UTC text."""
    if not isinstance(value, string_types) or not value:
        raise ValueError("GNIP posted time must be a non-empty string")
    match = UTC_TIMESTAMP_RE.match(value)
    if not match:
        raise ValueError("GNIP posted time must be an ISO-8601 UTC timestamp")
    timestamp = match.group(1)
    try:
        datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError("GNIP posted time contains an invalid calendar value")
    return timestamp
