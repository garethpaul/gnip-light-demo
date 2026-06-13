REDACTED_VALUE = "<redacted>"


def redacted_rule_payload(payload):
    """Return a diagnostic copy without query text or pagination tokens."""
    preview = dict(payload)
    for key in ("query", "next"):
        if key in preview:
            preview[key] = REDACTED_VALUE
    return preview
