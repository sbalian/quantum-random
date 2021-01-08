import pytest
import requests
import responses
import utils
from qrandom import _api


@responses.activate
def test_extract_data_success():

    responses.add(
        responses.GET,
        _api.URL,
        json={
            "type": "string",
            "length": 1024,
            "size": 8,
            "success": True,
            "data": utils.read_samples("hex")[0],
        },
        status=200,
    )
    response = requests.get(_api.URL)
    numbers = _api.extract_data(response)
    assert len(numbers) == 1024
    assert min(numbers) >= 0
    assert max(numbers) < 2 ** 64


@responses.activate
def test_extract_data_fail():
    responses.add(responses.GET, _api.URL, json={"success": False}, status=200)
    response = requests.get(_api.URL)
    with pytest.raises(RuntimeError):
        _api.extract_data(response)


def test_fetch():
    numbers = _api.fetch()
    assert len(numbers) == 1024
    assert min(numbers) >= 0
    assert max(numbers) < 2 ** 64
