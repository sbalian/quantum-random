import json
import os

import pytest
import responses

from qrandom import _api, _generator


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def test_responses():
    with open("tests/data/responses.json") as f:
        return json.load(f)


@pytest.fixture
def anu_url():
    return "https://api.quantumnumbers.anu.edu.au"


@pytest.fixture
def api_client_with_successful_api_call(
    mocked_responses, anu_url, test_responses
):
    mocked_responses.get(
        anu_url,
        json={"data": test_responses[0]["data"], "success": True},
        status=200,
    )
    return _api.Client("key")


@pytest.fixture
def api_client_with_failed_api_call(mocked_responses, anu_url):
    mocked_responses.get(
        anu_url,
        json={"success": False},
        status=400,
    )
    return _api.Client("key")


@pytest.fixture
def api_client_with_failed_api_call_and_no_json_response(
    mocked_responses, anu_url
):
    mocked_responses.get(
        anu_url,
        status=400,
    )
    return _api.Client("key")


@pytest.fixture
def api_client_with_failed_api_call_with_200_status(mocked_responses, anu_url):
    mocked_responses.get(
        anu_url,
        json={"success": False},
        status=200,
    )
    return _api.Client("key")


@pytest.fixture
def api_client_with_mocked_fetch_hex_raw(mocker, test_responses):
    mocker.patch(
        "qrandom._api.Client.fetch_hex_raw",
        return_value=test_responses[0],
    )
    return _api.Client("key")


@pytest.fixture
def mocked_environment(mocker):
    mocker.patch.dict(
        os.environ,
        {"QRANDOM_API_KEY": "key"},
    )


@pytest.fixture
def quantum_random_with_no_api_calls(mocked_environment):
    return _generator.QuantumRandom()


@pytest.fixture
def quantum_random_with_mocked_fetch_hex_raw(
    mocked_environment, mocker, test_responses
):
    mocker.patch(
        "qrandom._api.Client.fetch_hex_raw",
        return_value=test_responses[0],
    )
    return _generator.QuantumRandom()


@pytest.fixture
def quantum_random_with_mocked_fetch_hex_raw_twice(
    mocked_environment, mocker, test_responses
):
    mocker.patch(
        "qrandom._api.Client.fetch_hex_raw",
        side_effect=[test_responses[0], test_responses[1]],
    )
    return _generator.QuantumRandom()


@pytest.fixture
def quantum_random_with_mocked_fetch_hex_raw_five_times(
    mocked_environment, mocker, test_responses
):
    mocker.patch(
        "qrandom._api.Client.fetch_hex_raw",
        side_effect=[test_responses[i] for i in range(5)],
    )
    return _generator.QuantumRandom()


@pytest.fixture
def quantum_random_with_mocked_fetch_hex_raw_for_all_data(
    mocked_environment, mocker, test_responses
):
    mocker.patch(
        "qrandom._api.Client.fetch_hex_raw",
        side_effect=test_responses,
    )
    return _generator.QuantumRandom()
