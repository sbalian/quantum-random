import pytest

import qrandom._key


def test_get_from_env_success(monkeypatch):
    monkeypatch.setenv("QRANDOM_API_KEY", "key")
    assert qrandom._key.get_from_env() == "key"


def test_get_from_env_fail():
    with pytest.raises(qrandom._key.ApiKeyNotFoundInEnvError):
        qrandom._key.get_from_env()
