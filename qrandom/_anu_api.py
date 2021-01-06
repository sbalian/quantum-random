"""ANU API interface."""

from typing import Dict, List, Union

import requests


def fetch_quantum_rand_ints(length: int = 1024) -> List[int]:
    params: Dict[str, Union[int, str]] = {"length": length, "type": "uint16"}
    r = requests.get(
        "https://qrng.anu.edu.au/API/jsonI.php",
        params,
    )
    r.raise_for_status()
    r_json = r.json()
    if r_json["success"]:
        return r_json["data"]
    else:
        raise ConnectionError("ANU API failed (with a 200 status code)")
