from pathlib import Path

import click
from natsort import natsorted


@click.command()
@click.argument("folder", default=".", type=click.Path(exists=True, path_type=Path))
@click.option("-v", "--verbose", is_flag=True)
@click.option("--no-recursive", is_flag=True)
@click.option("--dry-run", is_flag=True)
@click.option("--sequence-start", default=2, show_default=True)
def cli(folder, verbose, no_recursive, dry_run, sequence_start):
    """Rename files using an ascending sequence of numbers.

    Applies to both the given folder and its subfolders.

    The order in which the files are named is determined by their natural sort order
    within their parent folder.

    The sequence is reset for every folder and begins with the value specified by
    '--sequence-start'.
    """

    if no_recursive:
        glob = folder.glob
    else:
        glob = folder.rglob

    files = [path for path in natsorted(glob("*")) if path.is_file()]

    # Only matters when the flag '--recursive' is passed.
    files_by_folder = {}
    for path in files:
        if path.parent not in files_by_folder:
            files_by_folder[path.parent] = []
        files_by_folder[path.parent].append(path)

    for folder, files in files_by_folder.items():
        for i, path in sorted(enumerate(files), reverse=True):
            new_stem = str(i + sequence_start)

            if dry_run or verbose:
                click.echo(f'Rename "{path.stem}" to "{new_stem} at: {path}')
                if dry_run:
                    continue
            path.replace(path.with_stem(new_stem))
