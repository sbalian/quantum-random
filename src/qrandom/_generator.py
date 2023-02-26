import random as pyrandom
import warnings
from typing import List, NoReturn

from qrandom import _api


class QuantumRandom(pyrandom.Random):
    """Quantum random number generator."""

    def __init__(self, batch_size: int = 1024):
        """Initializes an instance of QuantumRandom.

        batch_size is the number of ANU random numbers fetched and cached
        per API call (default is maximum allowed: 1024).

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            super().__init__()
        self._rand_int64: List[int] = []
        if not (0 < batch_size <= 1024):
            raise ValueError("batch_size must be > 0 and up to 1024")
        self.batch_size = batch_size
        return

    def fill(self, n: int = 1):
        """Fills the generator with n batches of 64-bit ints.

        The batch size is set during initialization.

        """
        for _ in range(n):
            self._rand_int64.extend(
                _api.get_qrand_int64(batch_size=self.batch_size)
            )
        return

    def _get_rand_int64(self) -> int:
        if not self._rand_int64:
            self.fill()
        return self._rand_int64.pop()

    def random(self) -> float:
        """Gets the next quantum random number in the range [0.0, 1.0)."""
        return self._get_rand_int64() / (2**64)

    def seed(self, *args, **kwds) -> None:
        """Method is ignored. There is no seed for the quantum vacuum.

        Raises RuntimeError if docstring for seed does not exist.

        """
        if self.seed.__doc__ is None:
            raise RuntimeError("Docstring for seed must exist.")
        warnings.warn(self.seed.__doc__)
        return

    def _notimplemented(self, *args, **kwds) -> NoReturn:
        """Method shouldn't be called for a quantum random number generator."""
        raise NotImplementedError("Quantum source does not have state.")
        return

    getstate = setstate = _notimplemented
