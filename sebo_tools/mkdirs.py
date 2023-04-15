from pathlib import Path

import click


@click.command()
@click.argument("number", type=int)
@click.option("-s", "--start-from", type=int)
def cli(number, start_from):
    """Create a given number of folders.

    The folders will be named using an ascending sequence of numbers starting from
    either '--start-from', the greatest integer used as the name of a subfolder, or 1.
    """

    folder = Path(".")

    if start_from is None:
        start_from = 1
        for path in folder.glob("*"):
            if path.is_dir() and path.stem.isdigit():
                start_from = max(int(path.stem) + 1, start_from)

    for folder_number in range(start_from, start_from + number):
        (folder / str(folder_number)).mkdir(exist_ok=True)
