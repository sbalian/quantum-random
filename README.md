# Quantum random numbers in Python

[![Tests](https://img.shields.io/github/actions/workflow/status/sbalian/quantum-random/tests.yml?label=tests
)](https://github.com/sbalian/quantum-random/actions/workflows/tests.yml)
[![Version](https://img.shields.io/pypi/v/quantum-random)](https://pypi.org/project/quantum-random/)
![Python Versions](https://img.shields.io/pypi/pyversions/quantum-random)
[![Download Stats](https://img.shields.io/pypi/dm/quantum-random)](https://pypistats.org/packages/quantum-random)
![License](https://img.shields.io/github/license/sbalian/quantum-random)

Use the [Python random module][pyrandom] with real quantum random numbers from
[ANU Quantum Numbers][anu].

## Usage

Import `qrandom` and use it like the standard `random` module:

```python
>>> import qrandom

>>> qrandom.random()
0.15357449726583722

>>> qrandom.sample(range(10), 2)
[6, 4]

>>> qrandom.gauss(0.0, 1.0)
-0.8370871276247828
```

You can also use the class `qrandom.QuantumRandom`. It has the same
interface as `random.Random`.

There is also a [NumPy][numpy] interface (implemented using [RandomGen][randomgen])
but it is not fully tested:

```python
>>> from qrandom.numpy import quantum_rng

>>> qrng = quantum_rng()

>>> qrng.random((3, 3))  # use like numpy.random.default_rng()
array([[0.37220278, 0.24337193, 0.67534826],
       [0.209068  , 0.25108681, 0.49201691],
       [0.35894084, 0.72219929, 0.55388594]])
```

## Installation

```bash
pip install quantum-random
```

The minimum supported version of Python is 3.9.

The NumPy interface is optional. To include it:

```bash
pip install 'quantum-random[numpy]'
```

## Setting the ANU Quantum Numbers API key

ANU Quantum Numbers requires an API key. You can get a free trial or pay for a key
[here][anupricing].

You can set the key in order of precedence as follows:

1. Set the `QRANDOM_API_KEY` environment variable.
2. Write the key to `qrandom.ini` using the `qrandom-init` setup utility (included with
the package). By default, the INI file is saved in your home config directory
(e.g., `~/.config/` in Linux) and `qrandom` will find it without you having to set
any environment variables. If you choose to save to a different location, you
must set `QRANDOM_CONFIG_DIR`.

The config file is ignored if `QRANDOM_API_KEY` is set.

## Pre-fetching batches

Quantum numbers are fetched from the API in batches of 1024 as needed. Use
`qrandom.fill(n)` to pre-fetch `n` batches at the start of your computation.

## Implementation details

The default pseudo-random generator is replaced by calls to
the ANU API. The `qrandom` module exposes a class derived from `random.Random` with a
`random()` method that outputs quantum floats in the range [0, 1)
(converted from 64-bit integers). Overriding `random.Random.random`
is sufficient to make the `qrandom` module behave mostly like the
`random` module as described in the [Python docs][pyrandom]. The exceptions
are `getrandbits()` and `randbytes()`: these are not available in
`qrandom`. Because `getrandbits()` is not available, `randrange()` cannot
produce arbitrarily long sequences. Finally, the user is warned when `seed()`
is called because the quantum generator has no state. For the same reason,
`getstate()` and `setstate()` are not implemented.

[anu]: https://quantumnumbers.anu.edu.au
[anupricing]: https://quantumnumbers.anu.edu.au/pricing
[pyrandom]: https://docs.python.org/3/library/random.html
[numpy]: https://numpy.org
[randomgen]: https://github.com/bashtage/randomgen
