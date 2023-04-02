import configparser
import os
import pathlib
import sys

import click
import xdg


@click.command()
def main() -> None:
    """This utility will help you set the API key for the qrandom package.

    You can get a key from https://quantumnumbers.anu.edu.au/pricing.

    """

    default_config_dir = xdg.xdg_config_home() / "qrandom"

    config_dir = click.prompt(
        "Where would you like to store the key?",
        type=pathlib.Path,
        default=default_config_dir,
    )
    config_dir = config_dir.expanduser().resolve()
    if config_dir.exists() and config_dir.is_file():
        click.echo(f"{config_dir} is not a directory.", err=True)
        sys.exit(1)
    config_path = config_dir / "qrandom.ini"
    if config_path.exists():
        click.confirm(
            f"Would you like to overwrite {config_path}?",
            abort=True,
        )

    config = configparser.ConfigParser()
    config.add_section("default")

    api_key = click.prompt(
        "Enter your API key",
        type=str,
    )

    os.makedirs(config_dir, exist_ok=True)
    config["default"]["key"] = api_key
    with open(config_path, "w") as f:
        config.write(f)
    print(f"Stored API key in {config_path}.")
    if config_dir != default_config_dir:
        click.echo(
            "Since you did not write to the default path, "
            f"do not forget to set QRANDOM_CONFIG_DIR to {config_dir}."
        )
    return
