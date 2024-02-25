# Quantum random numbers in Python

[![Tests](https://img.shields.io/github/actions/workflow/status/sbalian/quantum-random/tests.yml?label=tests
)](https://github.com/sbalian/quantum-random/actions/workflows/tests.yml)
[![Version](https://img.shields.io/pypi/v/quantum-random)](https://pypi.org/project/quantum-random/)
![Python Versions](https://img.shields.io/pypi/pyversions/quantum-random)
[![Download Stats](https://img.shields.io/pypi/dm/quantum-random)](https://pypistats.org/packages/quantum-random)
![License](https://img.shields.io/github/license/sbalian/quantum-random)

Use the [Python random module][pyrandom] with real quantum random numbers from
[ANU][anu]. The default pseudo-random generator is replaced by calls to
the ANU API.

## Usage

Import `qrandom` and use it like the standard `random` module. For example:

```python
>>> import qrandom

>>> qrandom.random()
0.15357449726583722

>>> qrandom.sample(range(10), 2)
[6, 4]

>>> qrandom.gauss(0.0, 1.0)
-0.8370871276247828
```

Alternatively, you can use the class `qrandom.QuantumRandom`. It has the same
interface as `random.Random`.

There is also a [NumPy][numpy] interface, although it is not fully tested:

```python
>>> from qrandom.numpy import quantum_rng

>>> qrng = quantum_rng()

>>> qrng.random((3, 3))  # use like numpy.random.default_rng()
array([[0.37220278, 0.24337193, 0.67534826],
       [0.209068  , 0.25108681, 0.49201691],
       [0.35894084, 0.72219929, 0.55388594]])
```

NumPy is supported using [RandomGen][randomgen].

## Installation

The minimum supported Python version is 3.8. Install with `pip`:

```bash
pip install -U quantum-random
```

If you want NumPy support:

```bash
pip install -U 'quantum-random[numpy]'
```

## First-time setup: setting your API key

ANU requires you to use an API key. You can get a free trial or pay for a key
[here][anupricing].

You can pass your key to `qrandom` in three ways:

1. By setting the environment variable `QRANDOM_API_KEY`.
2. By running the included command line utility `qrandom-init` to save your
key in `qrandom.ini` in a subdirectory of your home config directory
as specified by XDG, e.g., `/home/<your-username>/.config/qrandom/`.
3. By running `qrandom-init` to save your key in `qrandom.ini` in a directory
of your choice, and then specifying this directory by setting
`QRANDOM_CONFIG_DIR`.

If `QRANDOM_API_KEY` is set, its value is used as the API key and the
config file is not read. Otherwise, `qrandom` will look for the key
in the config directory. The config directory defaults to the XDG home config
and can be changed by setting `QRANDOM_CONFIG_DIR`.

## Pre-fetching batches

Batches of quantum numbers are fetched from the API as needed.
Each batch contains 1024 numbers. Use `qrandom.fill(n)` to fetch `n` batches
if you need to pre-fetch at the start of your computation.

## Tests

The tests run for Python 3.8 - 3.12 on the latest Windows,
macOS and Ubuntu runner images. Use [tox][tox] to run the tests locally.

See [here](./analysis/uniform.md) for a visualisation and a Kolmogorov–Smirnov
test.

## Notes on implementation

The `qrandom` module exposes a class derived from `random.Random` with a
`random()` method that outputs quantum floats in the range [0, 1)
(converted from 64-bit integers). Overriding `random.Random.random`
is sufficient to make the `qrandom` module behave mostly like the
`random` module as described in the [Python docs][pyrandom]. The exceptions
are `getrandbits()` and `randbytes()`: these are not available in
`qrandom`. Because `getrandbits()` is not available, `randrange()` cannot
produce arbitrarily long sequences. Finally, the user is warned when `seed()`
is called because the quantum generator has no state. For the same reason,
`getstate()` and `setstate()` are not implemented.

## License

See [LICENCE](./LICENSE).

[anu]: https://quantumnumbers.anu.edu.au
[anupricing]: https://quantumnumbers.anu.edu.au/pricing
[pyrandom]: https://docs.python.org/3/library/random.html
[tox]: https://tox.wiki/en/latest/
[numpy]: https://numpy.org
[randomgen]: https://github.com/bashtage/randomgen
