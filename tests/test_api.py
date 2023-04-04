import os

import pytest
import requests

from qrandom import _api


def test_client_url(anu_url):
    client = _api.Client()
    assert client.url == anu_url


def test_client_constructs_correctly_by_default():
    client = _api.Client()
    assert client.key is None
    assert client.params == {
        "length": 1024,
        "type": "hex16",
        "size": 4,
    }


def test_client_constructs_correctly_passing_batch_size():
    client = _api.Client(batch_size=10)
    assert client.key is None
    assert client.params == {
        "length": 10,
        "type": "hex16",
        "size": 4,
    }


def test_client_constructs_correctly_passing_key():
    client = _api.Client(key="key")
    assert client.key == "key"
    assert client.params == {
        "length": 1024,
        "type": "hex16",
        "size": 4,
    }


def test_fetch_hex_raw_returns_correctly(
    api_client_with_successful_api_call, test_responses
):
    r_json = api_client_with_successful_api_call.fetch_hex_raw()
    assert r_json == {"data": test_responses[0]["data"], "success": True}
    assert len(r_json["data"]) == 1024


def test_fetch_hex_raw_returns_correctly_with_set_batch_size(
    mocked_responses, test_responses, anu_url
):
    response = test_responses[0]
    response["length"] = 1023
    response["data"].pop()
    mocked_responses.get(
        anu_url,
        json={"data": response["data"], "success": True},
        status=200,
    )
    client = _api.Client("key", batch_size=1023)
    r_json = client.fetch_hex_raw()
    assert r_json == {"data": response["data"], "success": True}
    assert len(r_json["data"]) == 1023


def test_fetch_hex_raw_raises_when_api_key_not_found():
    client = _api.Client()
    with pytest.raises(RuntimeError) as exc_info:
        client.fetch_hex_raw()
    assert (
        exc_info.value.args[0]
        == "API key not set (set QRANDOM_API_KEY or run qrandom-init)"
    )


def test_fetch_hex_raw_raises_on_failed_api_call(
    api_client_with_failed_api_call,
):
    with pytest.raises(requests.HTTPError) as exc_info:
        api_client_with_failed_api_call.fetch_hex_raw()
    assert (
        exc_info.value.args[0]
        == "400 Client Error: Bad Request for url: https://api.quantumnumbers.anu.edu.au/?length=1024&type=hex16&size=4\nMore info: {'success': False}"  # noqa: E501
    )


def test_fetch_hex_raw_raises_on_failed_api_call_with_no_extra_json(
    api_client_with_failed_api_call_and_no_json_response,
):
    with pytest.raises(requests.HTTPError) as exc_info:
        api_client_with_failed_api_call_and_no_json_response.fetch_hex_raw()
    assert (
        exc_info.value.args[0]
        == "400 Client Error: Bad Request for url: https://api.quantumnumbers.anu.edu.au/?length=1024&type=hex16&size=4"  # noqa: E501
    )


def test_fetch_hex_raw_raises_on_failed_api_call_with_200_status(
    api_client_with_failed_api_call_with_200_status,
):
    with pytest.raises(requests.HTTPError) as exc_info:
        api_client_with_failed_api_call_with_200_status.fetch_hex_raw()
    assert (
        exc_info.value.args[0]
        == "the 'success' field in the ANU response was False even though the status code was 200"  # noqa: E501
    )


def test_fetch_hex_returns_hex_numbers_and_with_correct_length(
    api_client_with_mocked_fetch_hex_raw,
):
    numbers = api_client_with_mocked_fetch_hex_raw.fetch_hex()
    for number in numbers:
        int(number, 16)
    assert len(numbers) == 1024


def test_fetch_int64_returns_ints_and_with_correct_length(
    api_client_with_mocked_fetch_hex_raw,
):
    numbers = api_client_with_mocked_fetch_hex_raw.fetch_int64()
    for number in numbers:
        assert isinstance(number, int)
    assert len(numbers) == 1024


def test_fetch_int64_returns_in_correct_range(
    api_client_with_mocked_fetch_hex_raw,
):
    numbers = api_client_with_mocked_fetch_hex_raw.fetch_int64()
    for number in numbers:
        assert 0 <= number < 2**64


def test_find_api_key_directly_from_env():
    assert _api.find_api_key() == "key"


def test_find_api_key_from_default_config_dir(mocker, tmp_path):
    config_dir = tmp_path / "qrandom"
    config_dir.mkdir()
    environ = {
        name: value
        for name, value in os.environ.items()
        if name != "QRANDOM_API_KEY"
    }
    mocker.patch.dict(os.environ, environ, clear=True)
    with open(config_dir / "qrandom.ini", "w") as f:
        f.write("[default]\nkey = key-from-file\n")
    mocker.patch("xdg.xdg_config_home", return_value=tmp_path)
    assert _api.find_api_key() == "key-from-file"


def test_find_api_key_from_set_config_dir(mocker, tmp_path):
    config_dir = tmp_path / "qrandom"
    config_dir.mkdir()
    environ = {
        name: value
        for name, value in os.environ.items()
        if name != "QRANDOM_API_KEY"
    }
    environ["QRANDOM_CONFIG_DIR"] = str(config_dir)
    mocker.patch.dict(os.environ, environ, clear=True)
    with open(config_dir / "qrandom.ini", "w") as f:
        f.write("[default]\nkey = key-from-file\n")
    assert _api.find_api_key() == "key-from-file"


def test_find_api_key_returns_none_if_config_doesnt_exist_and_env_var_not_set(
    mocker, tmp_path
):
    config_dir = tmp_path / "qrandom"
    config_dir.mkdir()
    environ = {
        name: value
        for name, value in os.environ.items()
        if name != "QRANDOM_API_KEY"
    }
    environ["QRANDOM_CONFIG_DIR"] = str(config_dir)
    mocker.patch.dict(os.environ, environ, clear=True)
    assert _api.find_api_key() is None
