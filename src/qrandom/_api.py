import configparser
import os
import pathlib
from typing import Dict, List, Union

import requests
import xdg
from typing_extensions import TypedDict


def find_api_key() -> str:
    """Find the ANU API key.

    1. Return QRANDOM_API_KEY if defined.
    2. Get the config file directory from QRANDOM_CONFIG_DIR (defaulting to
       XDG home config directory if QRANDOM_CONFIG_DIR is not defined). Raise
       if the directory is not found.
    3. Return the key from the config file. Raise if the file is not found.

    """
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


class Response(TypedDict):
    success: bool
    type: str
    length: str
    data: List[str]


class Client:
    url = "https://api.quantumnumbers.anu.edu.au"

    def __init__(self, key: str, batch_size: int = 1024) -> None:
        """ANU API client.

        The API key can be obtained from https://quantumnumbers.anu.edu.au/pricing.
        batch_size is the number of numbers fetched (1024 by default).

        """  # noqa: E501
        self.headers: Dict[str, str] = {"x-api-key": key}
        self.params: Dict[str, Union[int, str]] = {
            "length": batch_size,
            "type": "hex16",
            "size": 4,
        }
        return

    def fetch_hex_raw(self) -> Response:
        """Gets hexadecimal random numbers from the ANU API.

        The output is the raw JSON from the API. Raises HTTPError if the ANU
        API call is not successful. This includes the case of
        batch_size > 1024.

        """
        response = requests.get(
            self.url, params=self.params, headers=self.headers
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            try:
                # Extend the error message with more info if available as JSON
                e.args = ((f"{e.args[0]}\nMore info: {e.response.json()}"),)
                raise e
            except requests.JSONDecodeError:
                raise e
        r_json = response.json()
        if not r_json["success"]:
            # This used to happen with the old API so keeping it here just
            # in case
            raise requests.HTTPError(
                "the 'success' field in the ANU response was False even "
                f"though the status code was {response.status_code}"
            )
        return r_json

    def fetch_hex(self) -> List[str]:
        """Gets hexadecimal random numbers from the ANU API.

        Calls Client.fetch_hex_raw(batch_size) and processes the response.

        """
        return self.fetch_hex_raw()["data"]

    def fetch_int64(self, batch_size: int = 1024) -> List[int]:
        """Gets random int64s from the ANU API.

        Calls Client.fetch_hex(batch_size) and converts the hex numbers to
        ints.

        """
        return [int(number, 16) for number in self.fetch_hex()]
