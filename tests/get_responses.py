#!/usr/bin/env python

import json

import requests

import qrandom


def main():
    json_responses = []
    num_hits = 10
    for hit in range(num_hits):
        print(f"Getting {hit+1} of {num_hits} ...")
        response = requests.get(qrandom._ANU_URL, qrandom._ANU_PARAMS)
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
