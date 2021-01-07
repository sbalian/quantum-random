"""ANU quantum random numbers.

Defines the QRN generator as a subclass of random.Random.

"""

import random
import warnings
from typing import Any, NoReturn

from . import _api


class QuantumRandom(random.Random):
    def __init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            super().__init__()
        self._rand_ints = []

    def _refresh_rand_ints(self) -> None:
        self._rand_ints = _api.fetch_quantum_rand_ints()

    def _rand_int(self) -> int:
        if not self._rand_ints:
            self._refresh_rand_ints()
        return self._rand_ints.pop()

    def random(self) -> float:
        return self._rand_int() / 65536

    def seed(self, a=None, version=None) -> None:
        warnings.warn("seed is ignored")

    def getstate(self) -> NoReturn:
        raise NotImplementedError

    def setstate(self, state: Any) -> NoReturn:
        raise NotImplementedError


_inst = QuantumRandom()
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
getrandbits = _inst.getrandbits
