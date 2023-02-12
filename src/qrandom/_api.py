from typing import Dict, List, Union

import requests

from qrandom import _key

ANU_URL = "https://api.quantumnumbers.anu.edu.au"


def get_qrand_int64(
    size: int = 1024, raw: bool = False
) -> Union[Dict[str, Union[bool, str, Dict[str, List[str]]]], List[int]]:
    """Gets quantum random int64s from the ANU API.

    size is the number of int64s fetched (1024 by default).

    raw = False (default) outputs a list of integers in base 10. Otherwise,
    the output is the raw JSON from the API (with the results nested and
    as hex strings).

    Raises HTTPError if the ANU API call is not successful.
    This includes the case of size > 1024.

    """
    params: Dict[str, Union[int, str]] = {
        "length": size,
        "type": "hex16",
        "size": 4,
    }
    headers: Dict[str, str] = {"x-api-key": _key.get_api_key()}
    response = requests.get(ANU_URL, params, headers=headers)
    try:
        response.raise_for_status()
    except requests.HTTPError as http_error:
        print("JSON response received:")
        print(response.json())
        raise http_error
    r_json = response.json()
    if not r_json["success"]:
        # This used to happen with the old API so keeping it here just in case.
        raise requests.HTTPError(
            "The 'success' field in the ANU response was False even "
            f"though the status code was {response.status_code}."
        )
    if raw:
        return r_json
    else:
        return [int(number, 16) for number in r_json["data"]]
