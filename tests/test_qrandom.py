import qrandom


def test_qrandom():
    population = [1, 100, 3, 4, 12]
    numbers = qrandom.sample(population, 2)
    assert len(numbers) == 2
    assert len(set(numbers)) == len(numbers)
    assert set(numbers).issubset(set(population))
