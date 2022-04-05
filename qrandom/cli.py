import configparser
import os
import pathlib
import sys

import xdg

DEFAULT_DIR = xdg.xdg_config_home()


def init():
    print(
        f"""\
This utility will help you set the API key for qrandom.
Where would you like to store the key?
Type in a directory path and press enter, or just press enter to
keep the default path [{DEFAULT_DIR}]:\
"""
    )
    user_input_dir = input().strip()
    if user_input_dir in ["", DEFAULT_DIR]:
        config_dir = DEFAULT_DIR
        config_path = config_dir / "qrandom.ini"
    else:
        config_dir = pathlib.Path(user_input_dir).expanduser().resolve()
        os.makedirs(config_dir, exist_ok=True)
        if config_dir.is_file():
            print(f"{config_dir} must be a directory.")
            sys.exit(1)
        config_path = config_dir / "qrandom.ini"
    if config_path.exists():
        print(
            f"""\
The file {config_path} exists. Would you like to overwrite? [Y/n]:\
"""
        )
        if input().strip().lower() not in ["y", "yes"]:
            print("Aborted.")
            sys.exit(1)
    config = configparser.ConfigParser()
    config.add_section("default")
    print("Enter your API key:")
    api_key = input().strip()
    config["default"]["key"] = api_key
    with open(config_path, "w") as f:
        config.write(f)
    print(f"Wrote to {config_path}.")
    if config_dir != DEFAULT_DIR:
        print(
            f"""
Since you did not write to the default path, do not forget to
set QRANDOM_CONFIG_DIR to {config_dir}.\
"""
        )
