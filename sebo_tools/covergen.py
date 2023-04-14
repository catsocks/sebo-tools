import json
from pathlib import Path

import click
import requests
from wand.image import Image

from . import validate_resolution

try:
    import rembg
except ImportError:
    rembg = None


@click.group(invoke_without_command=True)
@click.argument("folder", default=".", type=click.Path(exists=True, path_type=Path))
@click.option("--no-recursive", is_flag=True)
@click.option("-f", "--force", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("--dry-run", is_flag=True)
@click.option("-i", "--input", default="2.jpg", show_default=True)
@click.option("-o", "--output", default="1.png", show_default=True)
@click.option(
    "--max-resolution",
    default="1920x1920",
    show_default=True,
    type=click.UNPROCESSED,
    callback=validate_resolution,
)
@click.option(
    "--use-remove-bg", "bg_removal_tool", flag_value="remove.bg", default=True
)
@click.option("--use-rembg", "bg_removal_tool", flag_value="rembg")
@click.option("--remove-bg-api-key", envvar="REMOVE_BG_API_KEY")
def cli(folder, no_recursive, force, verbose, dry_run, **kwargs):
    """Generate product cover images.

    Search for images that match '--input' at the given folder and subfolders.

    For each matching image, the background is removed, it is scaled down if necessary
    to fit '--max-resolution', and then it is saved to '--output'.

    The output file will not be overwriten unless the '--force' flag is set.
    """

    if no_recursive:
        glob = folder.glob
    else:
        glob = folder.rglob

    remove_bg = get_bg_removal_fn(kwargs["bg_removal_tool"])

    input_path_str = kwargs["input"]
    path = None
    for path in glob(input_path_str):
        output_path = path.parent / kwargs["output"]
        if output_path.exists() and not force:
            click.secho(
                f"Not overriding file at: {output_path}."
                + " Pass '--force' to overwrite existing files.",
                fg="yellow",
            )
            continue

        with Image(filename=path) as img:
            blob = remove_bg(img.make_blob("jpg"), **kwargs)

        if dry_run or verbose:
            input_path = path.parent / input_path_str
            click.echo(
                f'Generate "{output_path}" from "{input_path}" at: ' + str(path.parent)
            )
            if dry_run:
                continue

        with Image(blob=blob) as img:
            max_width, max_height = kwargs["max_resolution"]
            img.transform(resize=f"{max_width}x{max_height}>")
            img.save(filename=output_path)

    if path is None:
        click.secho(
            "No images were found. "
            + "Use '--input PATH' to change the parent-folder-relative path to the "
            + "input images.",
            fg="yellow",
        )


def get_bg_removal_fn(tool):
    if tool == "remove.bg":
        return remove_bg_with_remove_bg
    elif tool == "rembg":
        if rembg is None:
            raise click.ClickException(
                "The background removal tool rembg is unavailable."
            )
        return remove_bg_with_rembg
    else:
        raise click.ClickException(f"The background removal tool {tool} is invalid.")


def remove_bg_with_remove_bg(blob, **kwargs):
    resp = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": blob},
        data={
            "size": "auto",
            "type": "product",
        },
        headers={"X-Api-Key": kwargs["remove_bg_api_key"]},
    )
    if resp.status_code == 200:
        return resp.content

    try:
        error_json = json.dumps(resp.json(), indent=4)
    except Exception:
        resp.raise_for_status()

    raise click.ClickException(
        "The Remove Background API request failed: \n"
        + error_json  # pyright: ignore reportUnboundVariable
    )


def remove_bg_with_rembg(blob, **kwargs):
    return rembg.remove(blob)
