import pytest
from qrandom import _quantum_random


@pytest.fixture
def quantum_random():
    return _quantum_random.QuantumRandom()


def test_get_state(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random.getstate()


def test_set_state(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random.setstate(None)


def test_seed(quantum_random):
    with pytest.warns(UserWarning):
        quantum_random.seed(42, 1)


def test_random(quantum_random):
    numbers = [
        [quantum_random.random() for _ in range(10)],
        [quantum_random.random() for _ in range(1200)],
    ]
    for numbers_ in numbers:
        assert min(numbers_) >= 0
        assert max(numbers_) < 1
    assert len(numbers[0]) == 10
    assert len(numbers[1]) == 1200
