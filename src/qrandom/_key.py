import configparser
import os
import pathlib

import xdg

INIT_MSG = "initialise qrandom.ini by running qrandom-init"


class ApiKeyNotFoundInEnvError(Exception):
    pass


class CustomConfigDirNotFoundError(Exception):
    pass


def get_from_env() -> str:
    try:
        return os.environ["QRANDOM_API_KEY"]
    except KeyError:
        raise ApiKeyNotFoundInEnvError


def get_custom_dir() -> pathlib.Path:
    try:
        config_dir = (
            pathlib.Path(os.environ["QRANDOM_CONFIG_DIR"])
            .expanduser()
            .resolve()
        )
        if not config_dir.exists():
            raise IOError(
                f"{config_dir} does not exist. {INIT_MSG.capitalize()}."
            )
        if config_dir.is_file():
            raise IOError(
                f"{config_dir} must be a directory. {INIT_MSG.capitalize()}."
            )
        return config_dir
    except KeyError:
        raise CustomConfigDirNotFoundError


def get_from_file(config_dir: pathlib.Path) -> str:
    config_path = config_dir / "qrandom.ini"
    if not config_path.exists():
        raise FileNotFoundError(
            f"{config_path} does not exist. {INIT_MSG.capitalize()}."
        )
    if config_path.is_dir():
        raise IsADirectoryError(
            f"{config_path} cannot be a directory.{INIT_MSG.capitalize()}."
        )
    config = configparser.ConfigParser()
    config.read(config_path)
    return config["default"]["key"]


def get_api_key() -> str:
    try:
        return get_from_env()
    except ApiKeyNotFoundInEnvError:
        try:
            config_dir = get_custom_dir()
        except CustomConfigDirNotFoundError:
            config_dir = xdg.xdg_config_home() / "qrandom"
    config_path = config_dir / "qrandom.ini"
    if not config_path.exists():
        raise FileNotFoundError(
            f"{config_path} does not exist. {INIT_MSG.capitalize()}."
        )
    if config_path.is_dir():
        raise IsADirectoryError(
            f"{config_path} cannot be a directory.{INIT_MSG.capitalize()}."
        )
    config = configparser.ConfigParser()
    config.read(config_path)
    return config["default"]["key"]
