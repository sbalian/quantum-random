import pytest
import requests
import responses
import utils
from qrandom import _anu_service


@responses.activate
def test_extract_data():

    responses.add(
        responses.GET,
        _anu_service.URL,
        json={
            "type": "string",
            "length": 1024,
            "size": 8,
            "success": True,
            "data": utils.read_samples("hex")[0],
        },
        status=200,
    )
    responses.add(
        responses.GET, _anu_service.URL, json={"success": False}, status=200
    )

    response = requests.get(_anu_service.URL)
    numbers = _anu_service.extract_data(response)
    assert len(numbers) == 1024
    assert min(numbers) >= 0
    assert max(numbers) < 2 ** 64

    response = requests.get(_anu_service.URL)
    with pytest.raises(RuntimeError):
        _anu_service.extract_data(response)
