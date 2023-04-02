"""Adds numpy support to qrandom."""

from typing import Any

import numpy.random
import randomgen

from qrandom import QuantumRandom


class ANUQRNG(QuantumRandom):
    def __init__(self, batch_size: int = 1024):
        super().__init__(batch_size=batch_size)

    def random_raw(self, voidp: Any) -> int:
        return self._get_rand_int64()


def quantum_rng():
    """Constructs a new Generator with a quantum BitGenerator (ANUQRNG)."""
    qrn = ANUQRNG()
    return numpy.random.Generator(randomgen.UserBitGenerator(qrn.random_raw))
