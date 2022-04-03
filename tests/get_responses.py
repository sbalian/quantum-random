#!/usr/bin/env python

import json
from typing import Dict, Union

import requests

import qrandom


def main():
    json_responses = []
    num_hits = 10
    for hit in range(num_hits):
        print(f"Getting {hit+1} of {num_hits} ...")
        params: Dict[str, Union[int, str]] = {
            "length": 1024,
            "type": "hex16",
            "size": 8,
        }
        response = requests.get(qrandom.ANU_URL, params)
        response.raise_for_status()
        json_r = response.json()
        json_responses.append(json_r)

    path = "data/responses.json"
    with open(path, "w") as f:
        json.dump(json_responses, f)
    print(f"Wrote to {path} .")

    return


if __name__ == "__main__":
    main()
