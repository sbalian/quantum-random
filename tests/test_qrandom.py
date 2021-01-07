import pytest
import qrandom


def read_sample_qrns():
    with open("tests/sample_qrns.txt") as f:
        samples = f.read().strip().split("\n")
    return [[int(s) for s in sample.split(",")] for sample in samples]


def test_qrandom():
    population = [1, 100, 3, 4, 12]
    numbers = qrandom.sample(population, 2)
    assert len(numbers) == 2
    assert len(set(numbers)) == len(numbers)
    assert set(numbers).issubset(set(population))


@pytest.fixture
def quantum_random():
    return qrandom.QuantumRandom()


def test_get_state(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random.getstate()


def test_set_state(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random.setstate(None)


def test_seed(quantum_random):
    with pytest.warns(UserWarning):
        quantum_random.seed(42, 1)


def test_random_short(mocker, quantum_random):
    mocker.patch(
        "qrandom._api.fetch_quantum_rand_ints",
        side_effect=read_sample_qrns(),
    )
    numbers = [
        [quantum_random.random() for _ in range(10)],
        [quantum_random.random() for _ in range(1200)],
    ]
    for numbers_ in numbers:
        assert min(numbers_) >= 0
        assert max(numbers_) < 1
    assert len(numbers[0]) == 10
    assert len(numbers[1]) == 1200