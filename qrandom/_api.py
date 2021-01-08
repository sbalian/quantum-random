"""ANU API interface."""

from typing import Dict, List, Union

import requests

PARAMS: Dict[str, Union[int, str]] = {
    "length": 1024,
    "type": "hex16",
    "size": 8,
}

URL: str = "https://qrng.anu.edu.au/API/jsonI.php"


def make_request(
    url: str = URL, params: Dict[str, Union[int, str]] = PARAMS
) -> requests.models.Response:
    response = requests.get(
        url,
        params,
    )
    return response


def extract_data(response: requests.models.Response) -> List[int]:
    response.raise_for_status()
    r_json = response.json()
    if r_json["success"]:
        return [int(number, 16) for number in r_json["data"]]
    else:
        raise RuntimeError(
            "ANU data extraction failed because 'success' in the response was False."  # noqa
        )
        # The status code is 200 when this happens


def fetch() -> List[int]:
    return extract_data(make_request())
