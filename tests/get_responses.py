import json

import qrandom


def main():
    json_responses = []
    num_hits = 10
    for hit in range(num_hits):
        print(f"Getting {hit+1} of {num_hits} ...")
        json_responses.append(qrandom._get_qrand_int64(size=1024, raw=True))

    path = "data/responses.json"
    with open(path, "w") as f:
        json.dump(json_responses, f)
    print(f"Wrote to {path} .")

    return


if __name__ == "__main__":
    main()
