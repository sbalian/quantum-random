"""ANU API interface."""

from typing import List

import requests


def fetch_quantum_rand_ints(length: int = 1024) -> List[int]:
    r = requests.get(
        "https://qrng.anu.edu.au/API/jsonI.php",
        {"length": length, "type": "uint16"},
    )
    r.raise_for_status()
    r_json = r.json()
    if r_json["success"]:
        return r_json["data"]
    else:
        raise ConnectionError("ANU API failed (with a 200 status code)")
