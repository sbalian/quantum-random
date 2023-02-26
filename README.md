# Quantum random numbers in Python

![Tests](https://github.com/sbalian/quantum-random/workflows/Tests/badge.svg)

Use the [Python random module][pyrandom] with real quantum random numbers from
[ANU][anu]. The default pseudo-random generator is replaced by calls to
the ANU API.

## Usage

Import `qrandom` and use it like the standard random module. For example:

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

Batches of quantum numbers are fetched from the API as needed.
Each batch contains 1024 numbers. Use `qrandom.fill(n)` to pre-fetch `n`
batches.

There is also a [NumPy][numpy] interface:

```python
>>> from qrandom.numpy import quantum_rng

>>> qrng = quantum_rng()

>>> qrng.random((3, 3))  # use like numpy.random.default_rng()
array([[0.37220278, 0.24337193, 0.67534826],
       [0.209068  , 0.25108681, 0.49201691],
       [0.35894084, 0.72219929, 0.55388594]])
```

## Installation

The minimum supported Python version is 3.7. Install with `pip`:

```bash
python -m pip install -U quantum-random
```

With NumPy support included:

```bash
python -m pip install -U quantum-random[numpy]
```

## First-time setup: passing your API key

ANU requires you to use an API key. You can get a free trial or paid key
from [here][anupricing].

You can pass your key to `qrandom` in three ways:

1. By setting the environment variable `QRANDOM_API_KEY`.
2. By running `qrandom-init` to save your key in an INI file
stored in a subdirectory of your home config directory as specified
by XDG, e.g., `/home/<your-username>/.config/qrandom/`.
3. By running `qrandom-init` to save your key in an INI file in a directory
of your choice set by `QRANDOM_CONFIG_DIR`.

`qrandom` will look for the key in the order above. The `qrandom-init`
command line utility is installed as part of the package.

## Tests

To run the tests locally, you will need [tox][tox] and Pythons 3.7 to 3.11
(i.e., multiple versions of Python installed and seen by tox using, e.g.,
[pyenv][pyenv] or [Homebrew][brew]). Then:

```bash
tox
```

See [here](./analysis/uniform.md) for a visualisation and a Kolmogorov–Smirnov
test.

## Notes on implementation

The `qrandom` module exposes a class derived from `random.Random` with a
`random()` method that outputs quantum floats in the range [0, 1)
(converted from 64-bit ints). Overriding `random.Random.random`
is sufficient to make the `qrandom` module behave mostly like the
`random` module as described in the [Python docs][pyrandom]. The exceptions
are `getrandbits()` and `randbytes()` that are not available in
`qrandom`. Because `getrandbits()` is not available, `randrange()` cannot
produce arbitrarily long sequences. Finally, the user is warned when `seed()`
is called because a quantum generator has no state. For the same reason,
`getstate()` and `setstate()` are not implemented.

NumPy is supported through [RandomGen][randomgen].

## License

See [LICENCE](./LICENSE).

[anu]: https://quantumnumbers.anu.edu.au
[anupricing]: https://quantumnumbers.anu.edu.au/pricing
[pyrandom]: https://docs.python.org/3/library/random.html
[tox]: https://tox.wiki/en/latest/
[pyenv]: https://github.com/pyenv/pyenv
[numpy]: https://numpy.org
[randomgen]: https://github.com/bashtage/randomgen
[brew]: https://brew.sh/
