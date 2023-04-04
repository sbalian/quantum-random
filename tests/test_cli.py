import configparser

import xdg
from click.testing import CliRunner

from qrandom import _cli


def test_default_flow(tmp_path, mocker):
    config_dir = tmp_path / ".config"
    mocker.patch("xdg.xdg_config_home", return_value=config_dir)
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(_cli.main, input="\nmy-key")
    assert result.exit_code == 0
    assert result.output == (
        "Where would you like to store the key? "
        f"[{config_dir / 'qrandom'}]: \n"
        "Enter your API key: my-key\n"
        f"Stored API key in {config_dir / 'qrandom/qrandom.ini'}.\n"
    )
    config = configparser.ConfigParser()
    config.read(config_dir / "qrandom/qrandom.ini")
    assert config["default"]["key"] == "my-key"


def test_user_provides_custom_dir(tmp_path):
    config_dir = tmp_path / "key-dir"
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(_cli.main, input=f"{config_dir}\nmy-key")
    assert result.exit_code == 0
    assert result.output == (
        "Where would you like to store the key? "
        f"[{xdg.xdg_config_home() / 'qrandom'}]: {config_dir}\n"
        "Enter your API key: my-key\n"
        f"Stored API key in {config_dir / 'qrandom.ini'}.\n"
        "Since you did not write to the default path, do not forget to "
        f"set QRANDOM_CONFIG_DIR to {config_dir}.\n"
    )
    config = configparser.ConfigParser()
    config.read(config_dir / "qrandom.ini")
    assert config["default"]["key"] == "my-key"


def test_quits_if_config_is_not_a_directory(tmp_path):
    config_path = tmp_path / "key"
    with open(config_path, "w") as f:
        f.write("xyz")
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(_cli.main, input=f"{config_path}")
    assert result.exit_code == 1
    assert result.output == (
        "Where would you like to store the key? "
        f"[{xdg.xdg_config_home() / 'qrandom'}]: {config_path}\n"
        f"{config_path} is not a directory.\n"
    )


def test_confirm_overwrite(tmp_path):
    config_dir = tmp_path / "key-dir"
    config_dir.mkdir()
    config_path = config_dir / "qrandom.ini"
    with open(config_path, "w") as f:
        f.write("xyz")
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(_cli.main, input=f"{config_dir}\ny\nmy-key")
    assert result.exit_code == 0
    assert result.output == (
        "Where would you like to store the key? "
        f"[{xdg.xdg_config_home() / 'qrandom'}]: {config_dir}\n"
        f"Would you like to overwrite {config_path}? [y/N]: y\n"
        "Enter your API key: my-key\n"
        f"Stored API key in {config_dir / 'qrandom.ini'}.\n"
        "Since you did not write to the default path, do not forget to "
        f"set QRANDOM_CONFIG_DIR to {config_dir}.\n"
    )
    config = configparser.ConfigParser()
    config.read(config_dir / "qrandom.ini")
    assert config["default"]["key"] == "my-key"


def test_do_not_overwrite(tmp_path):
    config_dir = tmp_path / "key-dir"
    config_dir.mkdir()
    config_path = config_dir / "qrandom.ini"
    with open(config_path, "w") as f:
        f.write("xyz")
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(_cli.main, input=f"{config_dir}\nn\nmy-key")
    assert result.exit_code == 1
    assert result.output == (
        "Where would you like to store the key? "
        f"[{xdg.xdg_config_home() / 'qrandom'}]: {config_dir}\n"
        f"Would you like to overwrite {config_path}? [y/N]: n\n"
        "Aborted!\n"
    )
