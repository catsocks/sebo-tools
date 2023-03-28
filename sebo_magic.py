from pathlib import Path

import click
import wand.image
from natsort import natsorted
from rembg import remove
from wand.image import Image


@click.group(chain=True)
@click.argument("folder", type=click.Path(exists=True))
@click.option(
    "--suffixes",
    multiple=True,
    default=[".jpg", ".jpeg", ".png", ".heic"],
    show_default=True,
)
@click.pass_context
def cli(ctx, folder, suffixes):
    """A set of commands that processes files matching the given suffixes in a given
    folder tree."""

    ctx.ensure_object(dict)
    ctx.obj["folder"] = Path(folder)
    ctx.obj["suffixes"] = suffixes


@cli.command()
@click.option("--sequence-start", default=2, show_default=True)
@click.pass_context
def rename(ctx, sequence_start):
    """Rename the files using a sequence of numbers based on the natural sort order
    of their filenames, starting from the value of '--sequence-start'."""

    files = []
    for path in ctx.obj["folder"].rglob("*"):
        if path.is_file() and path.suffix in ctx.obj["suffixes"]:
            files.append(path)

    folders = {}
    for path in natsorted(files):  # natural sort order
        if path.parent not in folders:
            folders[path.parent] = []
        folders[path.parent].append(path)

    for folder in folders:
        for i, path in reversed(list(enumerate(folders[folder]))):
            new_stem = str(i + sequence_start)
            path.replace(path.with_stem(new_stem))


@cli.command()
@click.option(
    "--format",
    default="jpg",
    help="Image format and file extension.",
    show_default=True,
)
@click.option("--max-resolution", default="1920x1920", show_default=True)
@click.option(
    "--auto-orient",
    default=True,
    type=bool,
    help="""Rotate the image based on its EXIF orientation attribute, so it's safe to
    use with programs that disregard this attribute.""",
    show_default=True,
)
@click.option("-f", "--force", is_flag=True)
@click.pass_context
def normalize(ctx, format, max_resolution, auto_orient, force):
    """Normalize the format, maximum resolution, and rotation of images.

    If a image fits the given normalization criteria, the function will not overwrite it
    unless the '--force' flag is set."""

    for path in ctx.obj["folder"].rglob("*"):
        if not path.is_file():
            continue

        if path.suffix not in ctx.obj["suffixes"]:
            continue

        with Image(filename=path) as img:
            img.format = format

            try:
                max_width, max_height = [int(s) for s in max_resolution.split("x")]
            except ValueError:
                max_width, max_height = 0, 0

            # Avoid marking the image as dirty.
            if img.width > max_width or img.height > max_height:
                img.transform(resize=max_resolution + ">")

            if auto_orient and img.orientation not in wand.image.ORIENTATION_TYPES[:2]:
                img.auto_orient()

            if img.dirty or force:
                img.save(filename=path)
                path.replace(path.with_suffix("." + format))


@cli.command()
@click.option("--input", default="2.jpg", show_default=True)
@click.option("--output", default="1.png", show_default=True)
@click.option("--max-resolution", default="1280x1280", show_default=True)
@click.option("-f", "--force", is_flag=True)
@click.pass_context
def create_cover(ctx, input, output, max_resolution, force):
    """Remove the background of, and resize if necessary, the images that match the
    given input path, saving them at the given output path relative to the folder
    they're in.

    If the output file already exists, the function will not overwrite it unless the
    '--force' flag is set.
    """

    for path in ctx.obj["folder"].rglob(input):
        output_path = path.parent / output
        if output_path.exists() and not force:
            click.secho(
                f"Not overriding {output_path}."
                + " Pass --force to change this behavior.",
                fg="yellow",
            )
            continue

        with Image(filename=path) as img:
            blob = remove(img.make_blob("png"))  # pyright: ignore
            with Image(blob=blob) as img:
                img.transform(resize=max_resolution + ">")
                img.save(filename=output_path)


@cli.command()
@click.option("--separator", default="\t")
@click.pass_context
def count(ctx, separator):
    """Print the number of files for each folder. Only files whose suffix match
    '--suffixes' are counted."""

    base_folder = ctx.obj["folder"]
    folders = {}
    for path in base_folder.rglob("*"):
        if path.suffix in ctx.obj["suffixes"]:
            if path.is_file():
                folders[path.parent] = folders.get(path.parent, 0) + 1

    for path, num_files in folders.items():
        relative_path = path.relative_to(
            base_folder.parent if path == base_folder else base_folder
        )
        click.echo(separator.join((relative_path.as_posix(), str(num_files))))
