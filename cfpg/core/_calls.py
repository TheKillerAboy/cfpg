import requests


def api_call(path, rest_method="get", params=None):
    params = {} if params is None else params

    request_method = getattr(requests, rest_method)
    url = f"https://codeforces.com/api/{path}"

    res = request_method(url, params=params).json()

    assert res["status"] == "OK"

    if "result" in res:
        return res["result"]

    return None
