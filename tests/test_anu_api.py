from qrandom import _anu_api


def test_fetch_quantum_rand_ints():
    numbers = _anu_api.fetch_quantum_rand_ints()
    assert len(numbers) == 1024
    assert min(numbers) >= 0
    assert max(numbers) <= 65535
    assert len(_anu_api.fetch_quantum_rand_ints(4)) == 4
