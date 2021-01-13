"""ANU quantum random numbers.

Defines the QRN generator as a subclass of random.Random.

"""

import random as pyrandom
import warnings
from typing import List, NoReturn

import requests

__all__ = [
    "seed",
    "random",
    "uniform",
    "triangular",
    "randint",
    "choice",
    "randrange",
    "sample",
    "shuffle",
    "choices",
    "normalvariate",
    "lognormvariate",
    "expovariate",
    "vonmisesvariate",
    "gammavariate",
    "gauss",
    "betavariate",
    "paretovariate",
    "weibullvariate",
    "getstate",
    "setstate",
]


_ANU_PARAMS = {
    "length": 1024,
    "type": "hex16",
    "size": 8,
}
_ANU_URL = "https://qrng.anu.edu.au/API/jsonI.php"


def _get_qrand_int64() -> List[int]:
    response = requests.get(_ANU_URL, _ANU_PARAMS)
    response.raise_for_status()
    r_json = response.json()

    if r_json["success"]:
        return [int(number, 16) for number in r_json["data"]]
    else:
        raise RuntimeError(
            "The 'success' field in the ANU response was False."
        )
        # The status code is 200 when this happens


class _QuantumRandom(pyrandom.Random):
    def __init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            super().__init__()
        self._rand_ints = []

    def _refresh_rand_ints(self) -> None:
        self._rand_ints = _get_qrand_int64()

    def _rand_int(self) -> int:
        if not self._rand_ints:
            self._refresh_rand_ints()
        return self._rand_ints.pop()

    def random(self) -> float:
        return self._rand_int() / (2 ** 64)

    def seed(self, *args, **kwds) -> None:
        warnings.warn(
            "Method is ignored. There is no seed for the quantum vacuum."
        )

    def _notimplemented(self, *args, **kwds) -> NoReturn:
        "Method should not be called for a quantum random number generator."
        raise NotImplementedError("Quantum source does not have state.")

    getstate = setstate = _notimplemented


_inst = _QuantumRandom()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
choices = _inst.choices
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
