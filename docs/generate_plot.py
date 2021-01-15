#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy import stats

import qrandom
import random


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


def kstest(data):
    quantum, python = data
    numbers, quantum_title = quantum
    py_numbers, python_title = python

    print(quantum_title, stats.kstest(numbers, "uniform"))
    print(python_title, stats.kstest(py_numbers, "uniform"))


def main():
    data = generate_data()
    plot(data)
    kstest(data)


if __name__ == "__main__":
    main()
