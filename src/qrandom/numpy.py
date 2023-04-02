"""Adds numpy support to qrandom."""

from typing import Any

import randomgen
from numpy import random as numpy_random

from . import _generator


class _ANUQRNG(_generator.QuantumRandom):
    def __init__(self, batch_size: int = 1024) -> None:
        super().__init__(batch_size=batch_size)
        return

    def random_raw(self, voidp: Any) -> int:
        return self._get_rand_int64()


def quantum_rng(batch_size: int = 1024):
    """Constructs a new Generator with a quantum BitGenerator (ANUQRNG).

    batch_size is the number of ANU random numbers fetched and cached
    per API call (default is maximum allowed: 1024).

    """
    qrn = _ANUQRNG(batch_size=batch_size)
    return numpy_random.Generator(randomgen.UserBitGenerator(qrn.random_raw))
