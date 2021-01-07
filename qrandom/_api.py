"""ANU API interface."""

from typing import Dict, List, Union

import requests


def fetch() -> List[int]:
    params: Dict[str, Union[int, str]] = {
        "length": 1024,
        "type": "hex16",
        "size": 8,
    }
    r = requests.get(
        "https://qrng.anu.edu.au/API/jsonI.php",
        params,
    )
    r.raise_for_status()
    r_json = r.json()
    if r_json["success"]:
        return [int(number, 16) for number in r_json["data"]]
    else:
        raise ConnectionError("ANU API failed (with a 200 status code)")
