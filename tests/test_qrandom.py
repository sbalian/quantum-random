import qrandom


def test_all_is_subset_of_everything_in_module():
    assert set(qrandom.__all__).issubset(set(dir(qrandom)))
