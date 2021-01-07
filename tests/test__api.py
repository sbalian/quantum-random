from qrandom import _api


def test_fetch_quantum_rand_ints():
    numbers = _api.fetch_quantum_rand_ints()
    assert len(numbers) == 1024
    assert min(numbers) >= 0
    assert max(numbers) <= 65535
