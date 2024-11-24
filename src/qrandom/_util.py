import pathlib


def xdg_config_home() -> pathlib.Path:
    return pathlib.Path.home() / ".config"
