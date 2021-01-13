import json

import pytest
import qrandom
from scipy import stats


def _read_mock_responses():
    with open("tests/data/responses.json") as f:
        return json.load(f)


@pytest.fixture
def quantum_random(requests_mock):
    mock_responses = []
    for response in _read_mock_responses():
        mock_responses.append(
            {"json": {"data": response["data"], "success": True}}
        )
    mock_responses.append(
        {
            "status_code": 500,
            "reason": "Exhausted mocks. Add more with tests/getresponses.",
        }
    )
    requests_mock.get(qrandom._ANU_URL, mock_responses)
    return qrandom._QuantumRandom()


def test__get_qrand_int64(requests_mock):
    requests_mock.get(
        qrandom._ANU_URL,
        json={
            "data": _read_mock_responses()[0]["data"],
            "success": True,
        },
    )
    numbers = qrandom._get_qrand_int64()
    assert len(numbers) == 1024
    assert min(numbers) >= 0
    assert max(numbers) < 2 ** 64

    requests_mock.get(
        qrandom._ANU_URL,
        json={
            "success": False,
        },
    )

    with pytest.raises(RuntimeError):
        numbers = qrandom._get_qrand_int64()


def test__notimplemented(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random._notimplemented(10, 100, x=1000)


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
    numbers = [quantum_random.random() for _ in range(10000)]
    assert min(numbers) >= 0
    assert max(numbers) < 1
    assert len(numbers) == 10000


def test_qrandom(quantum_random):
    population = [1, 100, 3, 4, 12]
    numbers = qrandom.sample(population, 2)
    assert len(numbers) == 2
    assert len(set(numbers)) == len(numbers)
    assert set(numbers).issubset(set(population))


def test_for_uniformity(quantum_random):
    numbers = [qrandom.random() for _ in range(10000)]
    assert stats.kstest(numbers, "uniform").statistic < 0.01
