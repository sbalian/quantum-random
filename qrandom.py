"""ANU quantum random numbers.

Implements a quantum random number generator as a subclass of random.Random
as described on https://docs.python.org/. The numbers come from the
ANU Quantum Random Number Generator at The Australian National University
(https://qrng.anu.edu.au/).

You can use it just like the standard random module (this module replaces the
default Mersenne Twister). But seeding is ignored and getstate() and setstate()
are not implemented because there is no state. Also, getrandbits() is not
yet available so randrange() can not cover arbitrarily large ranges.

"""

import random as pyrandom
import warnings
from typing import Dict, List, NoReturn, Union

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


_ANU_PARAMS: Dict[str, Union[int, str]] = {
    "length": 1024,
    "type": "hex16",
    "size": 8,
}
_ANU_URL: str = "https://qrng.anu.edu.au/API/jsonI.php"


def _get_qrand_int64() -> List[int]:
    """Get quantum random int64s from the ANU API."""
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
    """Quantum random number generator."""

    def __init__(self):
        """Initialize an instance."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            super().__init__()
        self._rand_int64 = []

    def random(self) -> float:
        """Get the next quantum random number in the range [0.0, 1.0)."""
        if not self._rand_int64:
            self._rand_int64 = _get_qrand_int64()
        rand_int64 = self._rand_int64.pop()
        return rand_int64 / (2 ** 64)

    def seed(self, *args, **kwds) -> None:
        "Method is ignored. There is no seed for the quantum vacuum."
        assert self.seed.__doc__ is not None
        warnings.warn(self.seed.__doc__)

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