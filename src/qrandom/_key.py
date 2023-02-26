import configparser
import os
import pathlib

import xdg


def get_api_key() -> str:
    api_key = os.getenv("QRANDOM_API_KEY")
    if api_key is not None:
        return api_key

    config_dir = (
        pathlib.Path(
            os.getenv("QRANDOM_CONFIG_DIR", xdg.xdg_config_home() / "qrandom")
        )
        .expanduser()
        .resolve()
    )

    if not config_dir.exists():
        raise FileNotFoundError(f"{config_dir} not found, run qrandom-init")
    if not config_dir.is_dir():
        raise NotADirectoryError(
            f"{config_dir} is not a directory, run qrandom-init"
        )
    config_path = config_dir / "qrandom.ini"
    if not config_path.exists():
        raise FileNotFoundError(f"{config_path} not found, run qrandom-init")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config["default"]["key"]
