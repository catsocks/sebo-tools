from pathlib import Path

import click


@click.command()
@click.argument("folder", type=click.Path(exists=True, path_type=Path))
@click.argument("number", type=int)
@click.option("--sequence-start", type=int)
def cli(folder, number, sequence_start):
    """Create a given number of folders.

    The folders will be named using an ascending sequence of numbers starting from 1 or
    '--sequence-start' or the greatest integer used as the name of a subfolder.
    """

    if sequence_start is None:
        sequence_start = 1
        for path in folder.glob("*"):
            if path.is_dir() and path.stem.isdigit():
                sequence_start = max(int(path.stem), sequence_start)

    for n in range(sequence_start, sequence_start + number):
        (folder / str(n)).mkdir(exist_ok=True)
