import json
import pathlib

import click

from qrandom import _api


@click.command()
@click.option(
    "--num-hits",
    "-n",
    type=int,
    default=10,
    show_default=True,
    help="Number of API calls.",
)
@click.option(
    "--output-directory",
    "-o",
    type=click.Path(
        exists=True,
        file_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    default=pathlib.Path("./data"),
    help="Output directory.",
    show_default=True,
)
def main(num_hits, output_directory) -> None:
    """Write a JSON file of responses from the ANU API for testing purposes."""

    output_path = output_directory / "responses.json"
    if output_path.exists():
        click.confirm(
            f"Would you like to overwrite {output_path}?",
            abort=True,
        )

    key = _api.find_api_key()
    client = _api.Client(key)

    click.echo("Fetching data ...")
    with click.progressbar(range(num_hits)) as bar:
        responses = [client.fetch_hex_raw() for _ in bar]
    click.echo("Writing responses ...")
    with open(pathlib.Path(output_path), "w") as f:
        json.dump(responses, f)
    click.echo(f"Wrote responses to {output_path} .")

    return


if __name__ == "__main__":
    main()
