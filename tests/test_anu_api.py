from qrandom import _anu_api


def test_fetch_quantum_random_numbers():
    numbers = _anu_api.fetch_quantum_random_numbers()
    assert len(numbers) == 1024
    assert min(numbers) >= 0
    assert max(numbers) <= 65535
    assert len(_anu_api.fetch_quantum_random_numbers(4)) == 4
