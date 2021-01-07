from qrandom import _api


def test_fetch():
    numbers = _api.fetch()
    assert len(numbers) == 1024
    assert min(numbers) >= 0
    assert max(numbers) < 2 ** 64
