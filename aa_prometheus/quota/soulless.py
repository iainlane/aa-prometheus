import json
import requests

ENDPOINT = "https://soulless.aa.net.uk/info.cgi"


def remaining():
    response = json.loads(
        requests.get(
            ENDPOINT, headers={"Accept": "application/json"}
        ).content.decode("UTF-8")
    )
    return response["quota_remaining"]
