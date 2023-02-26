import configparser
import os
import pathlib
import sys

import xdg

DEFAULT_DIR = xdg.xdg_config_home() / "qrandom"


def init() -> None:
    print(
        f"""\
This utility will help you set the API key for qrandom.

You can get a key from https://quantumnumbers.anu.edu.au/.

Where would you like to store the key?
[Default: {DEFAULT_DIR}]\
"""
    )
    user_input_dir = input().strip()
    if user_input_dir in ["", DEFAULT_DIR]:
        config_dir = DEFAULT_DIR
    else:
        config_dir = pathlib.Path(user_input_dir).expanduser().resolve()
        if config_dir.exists() and not config_dir.is_dir():
            print(f"{config_dir} must be a directory.")
            sys.exit(1)
    os.makedirs(config_dir, exist_ok=True)
    config_path = config_dir / "qrandom.ini"
    if config_path.exists():
        print(f"{config_path} exists. Would you like to overwrite it? [Y/n]")
        if input().strip() != "Y":
            print("Aborted.")
            sys.exit(1)
    config = configparser.ConfigParser()
    config.add_section("default")
    print("Enter your API key:")
    api_key = input().strip()
    config["default"]["key"] = api_key
    with open(config_path, "w") as f:
        config.write(f)
    print(f"Stored API key in {config_path}")
    if config_dir != DEFAULT_DIR:
        print(
            f"""
Since you did not write to the default path, do not forget to set
QRANDOM_CONFIG_DIR to {config_dir}\
"""
        )
    return
