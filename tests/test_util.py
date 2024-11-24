import pathlib

from qrandom import _util


def test_xdg_config_home():
    assert _util.xdg_config_home() == pathlib.Path.home() / ".config"
