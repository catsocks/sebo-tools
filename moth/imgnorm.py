"""
Normalize images in-place.
"""

import argparse
import logging
from pathlib import Path

from PIL import ExifTags, Image, ImageOps, UnidentifiedImageError

CONTAIN_SIZE = (1920, 1920)


def needs_transposing(image):
    im_exif = image.getexif()
    orientation = im_exif.get(ExifTags.Base.Orientation, 1)
    return orientation > 1


def needs_resizing(image):
    return image.width > CONTAIN_SIZE[0] or image.height > CONTAIN_SIZE[1]


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-v", "--verbose", action="store_true")


def main():
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    for path in Path().rglob("*"):
        if path.is_dir():
            continue

        try:
            with Image.open(path) as im:
                if "preview" in path.name:
                    # Thumbnails do not need normalization.
                    logging.info(f"{path}: skipping thumbnail")
                    continue

                if not (needs_transposing(im) or needs_resizing(im)):
                    logging.info(f"{path}: no changes necessary")

                # Some websites do not respect the EXIF Orientation so it's best to
                # not depend on it.
                new_im = ImageOps.exif_transpose(im)
                new_im = ImageOps.contain(im, (1920, 1920))
                new_im.save(path)
        except UnidentifiedImageError:
            logging.info(f"{path}: skipping irrelevant file")


if __name__ == "__main__":
    main()
