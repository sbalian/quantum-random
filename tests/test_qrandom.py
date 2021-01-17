import json

import pytest
from scipy import stats

import qrandom


def _read_mock_responses():
    with open("tests/data/responses.json") as f:
        return json.load(f)


MOCK_RESPONSES = _read_mock_responses()


@pytest.fixture
def quantum_random(requests_mock):
    mock_responses = []
    for response in MOCK_RESPONSES:
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
            "data": MOCK_RESPONSES[0]["data"],
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
        quantum_random._notimplemented()


def test_get_state(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random.getstate()


def test_set_state(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random.setstate()


def test_seed(quantum_random):
    with pytest.warns(UserWarning):
        quantum_random.seed()


def test_fill(quantum_random):
    assert not quantum_random._rand_int64
    quantum_random.fill()
    assert len(quantum_random._rand_int64) == 1024
    quantum_random.fill(2)
    assert len(quantum_random._rand_int64) == 3 * 1024


def test_random(quantum_random):
    assert not quantum_random._rand_int64
    number = quantum_random.random()
    assert len(quantum_random._rand_int64) == (1024 - 1)
    assert number >= 0.0
    assert number < 1.0
    numbers = [quantum_random.random() for _ in range(10000)]
    assert min(numbers) >= 0.0
    assert max(numbers) < 1.0
    assert len(numbers) == 10000
    assert len(quantum_random._rand_int64) == (10 * 1024 - 10000 - 1)


def test_for_uniformity(quantum_random):
    numbers = [qrandom.random() for _ in range(10000)]
    assert stats.kstest(numbers, "uniform").statistic < 0.01


def test___all__():
    assert set(qrandom.__all__).issubset(set(dir(qrandom)))
