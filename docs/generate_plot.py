import random
import sys

try:
    import matplotlib.pyplot as plt
    from scipy import stats
except ModuleNotFoundError:
    print(
        "To run this script, install with `poetry install -E analysis`."
        "Only Python 3.8 and 3.9 are supported."
    )
    sys.exit(1)


import qrandom


def generate_data():
    numbers = [qrandom.random() for _ in range(10000)]
    py_numbers = [random.random() for _ in range(10000)]
    return (numbers, "Quantum random"), (py_numbers, "Python pseudo-random")


def plot(data):
    quantum, python = data
    numbers, quantum_title = quantum
    py_numbers, python_title = python

    plt.figure(figsize=(8, 3))
    plt.subplot(1, 2, 1)
    plt.hist(numbers, edgecolor="black")
    plt.title(quantum_title)
    plt.subplot(1, 2, 2)
    plt.hist(py_numbers, edgecolor="black")
    plt.title(python_title)
    plt.tight_layout()
    plt.savefig("random.png", dpi=120, bbox_inches="tight")
    return


def kstest(data):
    quantum, python = data
    numbers, quantum_title = quantum
    py_numbers, python_title = python

    print(quantum_title, stats.kstest(numbers, "uniform"))
    print(python_title, stats.kstest(py_numbers, "uniform"))
    return


def main():
    data = generate_data()
    plot(data)
    kstest(data)
    return


if __name__ == "__main__":
    main()
