"""Adds numpy support to qrandom."""

import numpy.random
import randomgen  # type: ignore

from . import QuantumRandom


class ANUQRNG(QuantumRandom):
    def __init__(self):
        super().__init__()

    def random_raw(self, voidp) -> int:
        return self._get_rand_int64()


def quantum_rng():
    """Constructs a new Generator with a quantum BitGenerator (ANUQRNG)."""
    qrn = ANUQRNG()
    return numpy.random.Generator(randomgen.UserBitGenerator(qrn.random_raw))
