class ResponseShapeError(ValueError):
    pass


def response_results(payload):
    if not isinstance(payload, dict):
        raise ResponseShapeError("GNIP response must be an object")

    results = payload.get("results", [])
    if not isinstance(results, list):
        raise ResponseShapeError("GNIP response results must be a list")

    return results
