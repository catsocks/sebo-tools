from pathlib import Path

import click
from natsort import natsorted


@click.command()
@click.argument("folder", default=".", type=click.Path(exists=True, path_type=Path))
@click.option("--no-recursive", is_flag=True)
@click.option("--separator", default="\t")
def cli(folder, no_recursive, separator):
    """Count the number of files in folders.

    The number of files at the given folder and subfolders will be printed beside their
    path relative to the given folder.
    """

    if no_recursive:
        glob = folder.glob
    else:
        glob = folder.rglob

    count_by_folder = {}
    for path in glob("*"):
        if path.is_file():
            count_by_folder[path.parent] = count_by_folder.get(path.parent, 0) + 1

    for current_folder in natsorted(count_by_folder):
        relative_path = current_folder.relative_to(
            folder.parent if current_folder == folder else folder
        )
        click.echo(
            separator.join(
                (relative_path.as_posix(), str(count_by_folder[current_folder]))
            )
        )
