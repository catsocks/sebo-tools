#!/usr/bin/env python3
import argparse
import logging
import os
import tempfile
from pathlib import Path

from removebg import RemoveBg
from wand.image import Image

DEFAULT_IMAGE_SEQUENCE_START = 2

parser = argparse.ArgumentParser()
parser.add_argument("folder", type=Path)

subparsers = parser.add_subparsers(required=True, dest="action")

rename_images_parser = subparsers.add_parser("rename-images")
rename_images_parser.add_argument(
    "--sequence-start", default=DEFAULT_IMAGE_SEQUENCE_START
)

make_cover_parser = subparsers.add_parser("make-cover")
make_cover_parser.add_argument("--src", default="2.jpg")
make_cover_parser.add_argument("--dest", default="1.png")

print_image_urls_parser = subparsers.add_parser("print-image-urls")
print_image_urls_parser.add_argument("--base-url", required=True)

apply_images_orientation_parser = subparsers.add_parser("apply-images-orientation")


def rename_images(folder, sequence_start=DEFAULT_IMAGE_SEQUENCE_START):
    for i, path in enumerate(sorted(folder.iterdir())):
        new_stem = str(i + sequence_start)
        path.replace(path.with_stem(new_stem))


def apply_images_orientation(folder):
    """Rotate the image according to its EXIF oritentation attribute, because some
    marketplaces ignore this attribute when displaying images."""
    for path in folder.iterdir():
        with Image(filename=path) as img:
            if img.orientation not in ("top_left", "undefined"):
                img.auto_orient()
                img.save(filename=path)


def make_cover(removebg, folder, src, dest):
    dest_path = folder / dest
    if dest_path.exists():
        logging.info("A file already exists with the cover filename, skipping")
        return

    removebg.remove_background_from_img_file(
        folder / src, size="preview", type="product", new_file_name=dest_path
    )


def print_image_urls(folder, base_url):
    """Prefix the path to all files in a given folder with a given string, and print
    them divided by a space in a single line."""
    for path in sorted(folder.iterdir()):
        posix_path = path.relative_to(folder.parent).as_posix()
        print(f"{base_url}/{posix_path}", end=" ")
    print()


if __name__ == "__main__":
    args = parser.parse_args()

    if args.action == "rename-images":
        rename_images(args.folder, args.sequence_start)
    elif args.action == "apply-images-orientation":
        apply_images_orientation(args.folder)
    elif args.action == "make-cover":
        removebg = RemoveBg(
            os.environ["REMOVE_BG_API_KEY"],
            Path(tempfile.gettempdir()) / "removebg-error-log.txt",
        )
        make_cover(removebg, args.folder, args.src, args.dest)
    elif args.action == "print-image-urls":
        print_image_urls(args.folder, args.base_url)
