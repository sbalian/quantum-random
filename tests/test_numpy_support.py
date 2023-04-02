from qrandom import numpy


def test_numpy_support(mocked_environment, mocker, test_responses):
    mocker.patch(
        "qrandom._api.Client.fetch_hex_raw",
        side_effect=test_responses,
    )
    numbers = numpy.quantum_rng().random((3, 3))
    assert ((numbers >= 0.0) & (numbers < 1.0)).all()
    return
