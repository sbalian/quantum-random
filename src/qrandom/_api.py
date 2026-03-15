import configparser
import os
import pathlib
from typing import TypedDict

import requests

from qrandom import _exceptions, _util


def find_api_key() -> str:
    """Return the ANU API key. Raise APIKeyNotFoundError if the key is not found.

    - Return QRANDOM_API_KEY if defined.
    - Return the key from the config file $QRANDOM_CONFIG_DIR/qrandom.ini (using
      ~/.config/qrandom/qrandom.ini if QRANDOM_CONFIG_DIR is not defined).

    """
    api_key = os.getenv("QRANDOM_API_KEY")
    if api_key is not None:
        return api_key

    config_path = (
        pathlib.Path(
            os.getenv(
                "QRANDOM_CONFIG_DIR",
                (_util.xdg_config_home() / "qrandom").as_posix(),
            )
        )
        .expanduser()
        .resolve()
    ) / "qrandom.ini"

    if config_path.exists():
        config = configparser.ConfigParser()
        config.read(config_path)
        try:
            return config["default"]["key"]
        except KeyError as e:
            raise _exceptions.APIKeyNotFoundError(
                f"KeyError: '{e}' not found in config file. "
                "Format is an INI file with contents:\n\n"
                "[default]\n"
                "key=<your-api-key>\n\n"
                "Fix the file, set QRANDOM_API_KEY or run qrandom-init."
            )
    else:
        raise _exceptions.APIKeyNotFoundError(
            "API key not set (set QRANDOM_API_KEY or run qrandom-init)"
        )


class Response(TypedDict):
    success: bool
    type: str
    length: str
    data: list[str]


class Client:
    url = "https://api.quantumnumbers.anu.edu.au"

    def __init__(self, key: str, batch_size: int = 1024) -> None:
        """ANU API client.

        The API key can be obtained from https://quantumnumbers.anu.edu.au/pricing.
        batch_size is the number of numbers fetched (1024 by default).

        """
        self.key = key
        self.params: dict[str, int | str] = {
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
            self.url, params=self.params, headers={"x-api-key": self.key}
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

    def fetch_hex(self) -> list[str]:
        """Gets hexadecimal random numbers from the ANU API.

        Calls Client.fetch_hex_raw(batch_size) and processes the response.

        """
        return self.fetch_hex_raw()["data"]

    def fetch_int64(self) -> list[int]:
        """Gets random int64s from the ANU API.

        Calls Client.fetch_hex(batch_size) and converts the hex numbers to
        ints.

        """
        return [int(number, 16) for number in self.fetch_hex()]
