# Visualise and test if the quantum randoms are uniformly distributed in [0.0, 1)

Calling `qrandom.random()` 10,000 times, and comparing it to `random.random()`:

![Random](./random.png)

The [Kolmogorov–Smirnov statistics][kstest] with the reference distribution
`scipy.uniform` are 0.01 and 0.005 for the quantum and standard Python samples
respectively (using [`scipy.stats.kstest`][scipy-kstest]). The p-values
are 0.2 and 0.9 respectively for the quantum and standard cases respectively.

[kstest]: https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test
[scipy-kstest]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kstest.html
