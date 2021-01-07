"""Defines the QRN generator as a subclass of random.Random."""

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

    def _refresh_rand_ints(self, length: int = 1024) -> None:
        self._rand_ints = _api.fetch_quantum_rand_ints(length)

    def _rand_int(self) -> int:
        if not self._rand_ints:
            self._refresh_rand_ints(1024)
        return self._rand_ints.pop()

    def random(self) -> float:
        return self._rand_int() / 65536

    def seed(self, a=None, version=None) -> None:
        warnings.warn("seed is ignored")

    def getstate(self) -> NoReturn:
        raise NotImplementedError

    def setstate(self, state: Any) -> NoReturn:
        raise NotImplementedError
