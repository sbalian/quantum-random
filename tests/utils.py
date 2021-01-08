def _read_samples(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def _read_int_samples():
    return [
        [int(s) for s in sample.split(",")]
        for sample in _read_samples("tests/data/samples/ints.txt")
    ]


def _read_hex_samples():
    return [
        [s for s in sample.split(",")]
        for sample in _read_samples("tests/data/samples/hex.txt")
    ]


def read_samples(type_="int"):
    if type_ == "int":
        return _read_int_samples()
    elif type_ == "hex":
        return _read_hex_samples()
    else:
        raise ValueError(f"Unknown type '{type_}' for getting samples.")
