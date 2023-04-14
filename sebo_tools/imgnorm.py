from pathlib import Path

import click
import wand.image
from wand.image import Image

from . import validate_resolution


@click.command()
@click.argument("folder", default=".", type=click.Path(exists=True, path_type=Path))
@click.option("--no-recursive", is_flag=True)
@click.option("-f", "--force", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("--dry-run", is_flag=True)
@click.option("--format", default="jpg", show_default=True, help="Image format.")
@click.option("--extension", default="jpg", show_default=True, help="File extension.")
@click.option(
    "--max-resolution",
    default="1920x1920",
    show_default=True,
    type=click.UNPROCESSED,
    callback=validate_resolution,
)
def cli(folder, no_recursive, force, verbose, dry_run, **kwargs):
    """Normalize images in place.

    Normalize the file extension, format, maximum resolution, and orientation of images
    at the given folder and subfolders.

    If an image does not need to be normalized, the function will not overwrite it
    unless the '--force' flag is set.
    """

    if no_recursive:
        glob = folder.glob
    else:
        glob = folder.rglob

    max_width, max_height = kwargs["max_resolution"]

    for path in glob("*"):
        if not path.is_file():
            continue

        dry_run_changes = []
        with Image(filename=path) as img:
            if img.format != kwargs["format"]:
                dry_run_changes.append("format")
            img.format = kwargs["format"]

            if img.width > max_width or img.height > max_height:
                img.transform(resize=f"{max_width}x{max_height}>")
                dry_run_changes.append("max resolution")

            needs_rotation = img.orientation not in wand.image.ORIENTATION_TYPES[:2]
            if needs_rotation:
                img.auto_orient()
                dry_run_changes.append("rotation")

            expected_suffix = "." + kwargs["extension"]
            if path.suffix != expected_suffix:
                dry_run_changes.append("extension")

            if dry_run or verbose:
                changes_list = ", ".join(dry_run_changes)
                click.echo(f"Change {changes_list} for image: {path}")
                if dry_run:
                    continue

            if img.dirty or force:
                img.save(filename=path)

            if path.suffix != expected_suffix:
                path.replace(path.with_suffix(expected_suffix))
