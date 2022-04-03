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


def test_get_qrand_int64_returns_1024_nums(requests_mock):
    requests_mock.get(
        qrandom._ANU_URL,
        json={
            "data": MOCK_RESPONSES[0]["data"],
            "success": True,
        },
    )
    numbers = qrandom._get_qrand_int64()
    assert len(numbers) == 1024
    return


def test_get_qrand_int64_returns_0_or_more(requests_mock):
    requests_mock.get(
        qrandom._ANU_URL,
        json={
            "data": MOCK_RESPONSES[0]["data"],
            "success": True,
        },
    )
    numbers = qrandom._get_qrand_int64()
    assert min(numbers) >= 0
    return


def test_get_qrand_int64_returns_less_than_2_to_64(requests_mock):
    requests_mock.get(
        qrandom._ANU_URL,
        json={
            "data": MOCK_RESPONSES[0]["data"],
            "success": True,
        },
    )
    numbers = qrandom._get_qrand_int64()
    assert max(numbers) < 2**64
    return


def test_get_qrand_int64_raises_on_api_fail(requests_mock):
    requests_mock.get(
        qrandom._ANU_URL,
        json={
            "success": False,
        },
    )
    with pytest.raises(RuntimeError):
        qrandom._get_qrand_int64()
    return


def test_notimplemented_raises_on_call(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random._notimplemented()
    return


def test_get_state_raises_on_call(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random.getstate()
    return


def test_set_state_raises_on_call(quantum_random):
    with pytest.raises(NotImplementedError):
        quantum_random.setstate()
    return


def test_seed_warns_on_call(quantum_random):
    with pytest.warns(UserWarning):
        quantum_random.seed()
    return


def test_rand_int64_initially_empty(quantum_random):
    assert not quantum_random._rand_int64
    return


def test_rand_int64_has_1024_nums_after_call_to_fill(quantum_random):
    quantum_random.fill()
    assert len(quantum_random._rand_int64) == 1024
    return


def test_rand_int64_has_2048_nums_after_2_calls_to_fill(quantum_random):
    quantum_random.fill(2)
    assert len(quantum_random._rand_int64) == 2048
    return


def test_rand_int64_has_1023_nums_after_call_to_random(quantum_random):
    quantum_random.random()
    assert len(quantum_random._rand_int64) == (1024 - 1)
    return


def test_random_returns_in_correct_range(quantum_random):
    number = quantum_random.random()
    assert number >= 0.0
    assert number < 1.0
    return


def test_random_returns_in_correct_range_for_many_calls(quantum_random):
    numbers = [quantum_random.random() for _ in range(10000)]
    assert min(numbers) >= 0.0
    assert max(numbers) < 1.0


def test_random_returns_correct_num_of_nums_for_many_calls(quantum_random):
    numbers = [quantum_random.random() for _ in range(10000)]
    assert len(numbers) == 10000
    return


def test_random_returns_uniform_distribution(quantum_random):
    numbers = [qrandom.random() for _ in range(10000)]
    assert stats.kstest(numbers, "uniform").statistic < 0.01
    return


def test_all_is_subset_of_everything_in_module():
    assert set(qrandom.__all__).issubset(set(dir(qrandom)))
    return
