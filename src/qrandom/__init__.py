"""ANU Quantum Random Numbers.

Implements a quantum random number generator as a subclass of random.Random
as described on https://docs.python.org/3/library/random.html. The numbers
come from the ANU Quantum Random Number Generator at The Australian National
University (https://quantumnumbers.anu.edu.au/).

You can use this module just like the standard random module. The module
replaces the default Mersenne Twister generator. Seeding is ignored
and getstate() and setstate() are not implemented because there is no state.
Also, getrandbits() is not available so randrange() can't cover arbitrarily
large ranges. There is no randbytes() because getrandbits() is not available.

"""

import sys

from ._generator import QuantumRandom

__all__ = [
    "QuantumRandom",
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


_inst = QuantumRandom()
betavariate = _inst.betavariate

if (sys.version_info.major, sys.version_info.minor) >= (3, 12):
    binomialvariate = _inst.binomialvariate  # type: ignore[attr-defined]
    __all__.append("binomialvariate")

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
