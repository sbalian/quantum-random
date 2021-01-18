# Quantum random numbers in Python

![Tests](https://github.com/sbalian/quantum-random/workflows/Tests/badge.svg)

This package brings the [ANU quantum random numbers][anu] to Python 3.6+.

The default pseudo-random generator in Python is replaced by calls to the
ANU API that serves real quantum random numbers.

## Install

```bash
pip install quantum-random
```

## Usage

Just import `qrandom` and use it like you'd use the
[standard Python random module][pyrandom]. For example,

```python
>>> import qrandom

>>> qrandom.random()
0.15357449726583722

>>> qrandom.sample(range(10), 2)
[6, 4]

>>> qrandom.gauss(0.0, 1.0)
-0.8370871276247828
```

Under the hood, batches of quantum numbers are fetched from the API as needed
and each batch contains 1024 numbers. If you wish to pre-fetch more, use
`qrandom.fill(n)`, where `n` is the number of batches.

## Notes on implementation

The `qrandom` module exposes a class derived from `random.Random` with a
`random()` method that outputs quantum floats in the range [0, 1)
(converted from 64-bit ints). Overriding `random.Random.random`
is sufficient to make the `qrandom` module behave mostly like the
`random` module as described in the [Python docs][pyrandom]. The exceptions
at the moment are `getrandbits()` and `randbytes()` that are not available in
`qrandom`. Because `getrandbits()` is not available, `randrange()` cannot
produce arbitrarily long sequences. Finally, the user is warned when `seed()`
is called because there is no state. For the same reason, `getstate()` and
`setstate()` are not implemented.

## Tests

To run the tests locally, you will need [poetry][poetry] and Python 3.6-3.9.

```bash
poetry install
poetry run tox
```

See [here](./docs/uniform.md) for a visualisation and a Kolmogorov–Smirnov test.

## License

See [LICENCE](./LICENSE).

[anu]: https://qrng.anu.edu.au
[pyrandom]: https://docs.python.org/3.9/library/random.html
[poetry]: https://python-poetry.org
