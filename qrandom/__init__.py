"""ANU quantum random numbers.

Implements a quantum random number generator as a subclass of random.Random
as described on https://docs.python.org/. The numbers come from the
ANU Quantum Random Number Generator at The Australian National University
(https://quantumnumbers.anu.edu.au/).

You can use it just like the standard random module (this module replaces the
default Mersenne Twister). But seeding is ignored and getstate() and setstate()
are not implemented because there is no state. Also, getrandbits() is not
yet available so randrange() can not cover arbitrarily large ranges. Finally,
because getrandbits() is not available, there is no randbytes() (new in
Python 3.9).

"""

import configparser
import os
import pathlib
import random as pyrandom
import warnings
from typing import Dict, List, NoReturn, Union

import requests
import xdg

__version__ = "1.1.1"

__all__ = [
    "betavariate",
    "choice",
    "choices",
    "expovariate",
    "gammavariate",
    "gauss",
    "getstate",
    "lognormvariate",
    "normalvariate",
    "paretovariate",
    "randint",
    "random",
    "randrange",
    "sample",
    "seed",
    "setstate",
    "shuffle",
    "triangular",
    "uniform",
    "vonmisesvariate",
    "weibullvariate",
    "fill",
]

_ANU_URL = "https://api.quantumnumbers.anu.edu.au"


def _get_api_key() -> str:
    init_msg = "initialise qrandom.ini by running qrandom-init"
    # 1 QRANDOM_API_KEY env var
    try:
        return os.environ["QRANDOM_API_KEY"]
    except KeyError:
        # 2 qrandom.ini in directory defined by QRANDOM_CONFIG_DIR env var
        try:
            config_dir = (
                pathlib.Path(os.environ["QRANDOM_CONFIG_DIR"])
                .expanduser()
                .resolve()
            )
            if not config_dir.exists():
                raise IOError(
                    f"{config_dir} does not exist. "
                    f"{init_msg.capitalize()}."
                )
            if config_dir.is_file():
                raise IOError(
                    f"{config_dir} must be a directory. "
                    f"{init_msg.capitalize()}."
                )
            config_path = config_dir / "qrandom.ini"
            if not config_path.exists():
                raise FileNotFoundError(
                    f"{config_path} does not exist. "
                    f"{init_msg.capitalize()}."
                )
            if config_path.is_dir():
                raise IsADirectoryError(
                    f"{config_path} cannot be a directory."
                    f"{init_msg.capitalize()}."
                )
        # 3 qrandom.ini in default directory (<xdg-home>/qrandom.ini)
        except KeyError:
            config_path = xdg.xdg_config_home() / "qrandom.ini"
            if not config_path.exists():
                raise FileNotFoundError(
                    f"{config_path} does not exist. "
                    "Set the environment variable QRANDOM_API_KEY or "
                    f"{init_msg}. "
                    "You may also set QRANDOM_CONFIG_DIR to change the "
                    "default directory containing qrandom.ini."
                )
            if config_path.is_dir():
                raise IsADirectoryError(
                    f"{config_path} cannot be a directory."
                    f"{init_msg.capitalize()}."
                )
        config = configparser.ConfigParser()
        config.read(config_path)
        return config["default"]["key"]


def _get_qrand_int64(size: int = 1024) -> List[int]:
    """Gets quantum random int64s from the ANU API.

    size is the number of int64s fetched (1024 by default).

    Raises RuntimeError if the ANU API call is not successful. This includes
    the case of size > 1024.

    """
    params: Dict[str, Union[int, str]] = {
        "length": size,
        "type": "hex16",
        "size": 4,
    }
    headers: Dict[str, str] = {"x-api-key": _get_api_key()}
    response = requests.get(_ANU_URL, params, headers=headers)
    response.raise_for_status()
    r_json = response.json()

    if r_json["success"]:
        return [int(number, 16) for number in r_json["data"]]
    else:
        raise RuntimeError(
            "The 'success' field in the ANU response was False."
        )
        # The status code is 200 when this happens
    return


class QuantumRandom(pyrandom.Random):
    """Quantum random number generator."""

    def __init__(self):
        """Initializes an instance of QuantumRandom."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            super().__init__()
        self._rand_int64 = []
        return

    def fill(self, n: int = 1):
        """Fills the generator with n batches of 1024 64-bit ints."""
        for _ in range(n):
            self._rand_int64.extend(_get_qrand_int64())
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


_inst = QuantumRandom()
betavariate = _inst.betavariate
choice = _inst.choice
choices = _inst.choices
expovariate = _inst.expovariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
getstate = _inst.getstate
lognormvariate = _inst.lognormvariate
normalvariate = _inst.normalvariate
paretovariate = _inst.paretovariate
randint = _inst.randint
random = _inst.random
randrange = _inst.randrange
sample = _inst.sample
seed = _inst.seed
setstate = _inst.setstate
shuffle = _inst.shuffle
triangular = _inst.triangular
uniform = _inst.uniform
vonmisesvariate = _inst.vonmisesvariate
weibullvariate = _inst.weibullvariate
fill = _inst.fill
