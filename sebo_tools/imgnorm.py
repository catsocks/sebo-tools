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
@click.option("--format", default="jpeg", show_default=True, help="Image format.")
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

        dry_run_actions = []
        with Image(filename=path) as original:
            with original.convert(kwargs["format"]) as img:
                if img.width > max_width or img.height > max_height:
                    img.transform(resize=f"{max_width}x{max_height}>")
                    dry_run_actions.append("shrink")

                if img.orientation not in ["undefined", "top_left"]:
                    img.auto_orient()
                    dry_run_actions.append("rotate")

                is_format_different = original.format != img.format
                if is_format_different:
                    dry_run_actions.append(f"convert format from {original.format} to "
                        + str(img.format))

                if is_format_different or img.dirty or force:
                    if not dry_run:
                        img.save(filename=path)

        expected_suffix = "." + kwargs["extension"]
        if path.suffix != expected_suffix:
            if not dry_run:
                path.replace(path.with_suffix(expected_suffix))
            dry_run_actions.append(f"change suffix from {path.suffix} to " 
                + expected_suffix)

        if (dry_run or verbose) and dry_run_actions:
            msg = ", ".join(dry_run_actions).capitalize()
            click.echo(f"{msg}: {path}")
