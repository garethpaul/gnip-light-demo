import json


class ResponseShapeError(ValueError):
    pass


def decode_response_payload(payload):
    try:
        decoded = json.loads(payload)
    except (TypeError, ValueError, RuntimeError, OverflowError):
        raise ResponseShapeError("GNIP response must contain valid JSON")
    if not isinstance(decoded, dict):
        raise ResponseShapeError("GNIP response must be an object")
    return decoded


def response_results(payload):
    if not isinstance(payload, dict):
        raise ResponseShapeError("GNIP response must be an object")

    results = payload.get("results", [])
    if not isinstance(results, list):
        raise ResponseShapeError("GNIP response results must be a list")
    if any(not isinstance(result, dict) for result in results):
        raise ResponseShapeError("GNIP response result items must be objects")

    return results
