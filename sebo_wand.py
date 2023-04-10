from pathlib import Path

import click
import wand.image
from natsort import natsorted
from rembg import remove
from wand.image import Image


@click.group(chain=True)
@click.argument("folder", type=click.Path(exists=True))
@click.option(
    "--suffix",
    multiple=True,
    default=[".jpg", ".jpeg", ".png", ".heic"],
    show_default=True,
)
@click.pass_context
def cli(ctx, folder, suffix):
    """Commands for organizing and processing files that match '--suffix' in the
    given folder and its subfolders.
    """

    ctx.ensure_object(dict)
    ctx.obj["folder"] = Path(folder)
    ctx.obj["suffix"] = suffix


@cli.command()
@click.option("--sequence-start", default=2, show_default=True)
@click.pass_context
def rename(ctx, sequence_start):
    """Rename files using an ascending sequence of numbers.

    The order which a file is assigned a number from the sequence is determined by
    their natural sort order in their parent folder.

    The sequence starts from the value of '--sequence-start' for every folder.
    """

    files = []
    for path in ctx.obj["folder"].rglob("*"):
        if path.is_file() and path.suffix in ctx.obj["suffix"]:
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
    """Normalize images.

    The format, maximum resolution, rotation, and file extension will be normalized.

    If a image fits the given normalization criteria, the function will not overwrite it
    unless the '--force' flag is set.
    """

    for path in ctx.obj["folder"].rglob("*"):
        if not path.is_file():
            continue

        if path.suffix not in ctx.obj["suffix"]:
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

            target_suffix = "." + format
            if path.suffix == target_suffix or img.dirty or force:
                img.save(filename=path)
                path.replace(path.with_suffix(target_suffix))


@cli.command()
@click.option("--input", default="2.jpg", show_default=True)
@click.option("--output", default="1.png", show_default=True)
@click.option("--max-resolution", default="1280x1280", show_default=True)
@click.option("-f", "--force", is_flag=True)
@click.pass_context
def create_cover(ctx, input, output, max_resolution, force):
    """Generate the "product cover" version of images.

    Remove the background of, and resize if necessary, images that match the given
    '--input' path relative to their parent folder. The new images will be saved at the
    given '--output' path relative to their parent folder.

    If a file already exists at an output path, it will not be overwriten unless the
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
    """Print the number of files in folders.

    The given folder and all of its subfolders are included. And **only** files whose
    suffix match '--suffix' are counted.
    """

    base_folder = ctx.obj["folder"]
    folders = {}
    for path in base_folder.rglob("*"):
        if path.suffix in ctx.obj["suffix"]:
            if path.is_file():
                folders[path.parent] = folders.get(path.parent, 0) + 1

    for folder in natsorted(folders):
        relative_path = folder.relative_to(
            base_folder.parent if folder == base_folder else base_folder
        )
        num_files = folders[folder]
        click.echo(separator.join((relative_path.as_posix(), str(num_files))))


@cli.command()
@click.argument("num-dirs", type=int)
@click.option("--sequence-start", default=1, show_default=True)
@click.pass_context
def mkdirs(ctx, num_dirs, sequence_start):
    """Create a given number of directories.

    The folders will be created at the root of the given folder, and they will be
    named them based on an ascending sequence of numbers starting from the value of
    '--sequence-start'.
    """

    for n in range(sequence_start, sequence_start + num_dirs):
        (ctx.obj["folder"] / str(n)).mkdir(exist_ok=True)
