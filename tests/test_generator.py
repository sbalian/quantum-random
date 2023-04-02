import pytest

from qrandom import _generator


def test_notimplemented_raises_on_call(quantum_random_with_no_api_calls):
    with pytest.raises(NotImplementedError) as exc_info:
        quantum_random_with_no_api_calls._notimplemented()
    assert exc_info.value.args[0] == "quantum source does not have state"


def test_get_state_raises_on_call(quantum_random_with_no_api_calls):
    with pytest.raises(NotImplementedError) as exc_info:
        quantum_random_with_no_api_calls.getstate()
    assert exc_info.value.args[0] == "quantum source does not have state"


def test_set_state_raises_on_call(quantum_random_with_no_api_calls):
    with pytest.raises(NotImplementedError) as exc_info:
        quantum_random_with_no_api_calls.setstate()
    assert exc_info.value.args[0] == "quantum source does not have state"


def test_seed_warns_on_call(quantum_random_with_no_api_calls):
    with pytest.warns(
        UserWarning, match=quantum_random_with_no_api_calls.seed.__doc__
    ):
        quantum_random_with_no_api_calls.seed()


def test_fill_gets_1024_nums(quantum_random_with_mocked_fetch_hex_raw):
    quantum_random_with_mocked_fetch_hex_raw.fill()
    assert len(quantum_random_with_mocked_fetch_hex_raw._rand_int64) == 1024


def test_fill_gets_2048_nums_after_two_calls(
    quantum_random_with_mocked_fetch_hex_raw_twice,
):
    quantum_random_with_mocked_fetch_hex_raw_twice.fill(2)
    assert (
        len(quantum_random_with_mocked_fetch_hex_raw_twice._rand_int64) == 2048
    )


def test_get_rand_int64(quantum_random_with_mocked_fetch_hex_raw_five_times):
    for call in range(1024 * 5):
        quantum_random_with_mocked_fetch_hex_raw_five_times._get_rand_int64()
        assert (
            len(
                quantum_random_with_mocked_fetch_hex_raw_five_times._rand_int64
            )
            == (1024 - call - 1) % 1024
        )


def test_rand_int64_has_1023_nums_after_call_to_random(
    quantum_random_with_mocked_fetch_hex_raw,
):
    quantum_random_with_mocked_fetch_hex_raw.random()
    assert len(quantum_random_with_mocked_fetch_hex_raw._rand_int64) == 1023


def test_random_returns_in_correct_range(
    quantum_random_with_mocked_fetch_hex_raw_for_all_data,
):
    for _ in range(1024 * 10):
        number = quantum_random_with_mocked_fetch_hex_raw_for_all_data.random()
        assert number >= 0.0
        assert number < 1.0


def test_quantum_random_constructs_correctly_by_default(mocked_environment):
    quantum_random = _generator.QuantumRandom()
    assert not quantum_random._rand_int64
    assert quantum_random._api_client.headers == {"x-api-key": "key"}
    assert quantum_random._api_client.params == {
        "length": 1024,
        "type": "hex16",
        "size": 4,
    }


def test_quantum_random_raises_for_batch_size_out_of_bounds(
    mocked_environment,
):
    with pytest.raises(ValueError) as exc_info:
        _generator.QuantumRandom(batch_size=-1)
    assert exc_info.value.args[0] == "batch_size must be > 0 and up to 1024"
    with pytest.raises(ValueError) as exc_info:
        _generator.QuantumRandom(batch_size=1025)
    assert exc_info.value.args[0] == "batch_size must be > 0 and up to 1024"
