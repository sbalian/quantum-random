# Quantum random numbers in Python

This package brings the [ANU quantum random numbers][anu] to Python.

```bash
pip install quantum-random
```

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

Only Python 3.6+ are supported.

[This notebook][viz] shows the distribution obtained by calling the uniform
random method for [0.0, 1.0) (`qrandom.random()`) and checks for uniformity
using a Kolmogorov-Smirnov test.

[anu]: https://qrng.anu.edu.au
[pyrandom]: https://docs.python.org/3.9/library/random.html
[viz]: ./tests/notebooks/UniformTest.ipynb
