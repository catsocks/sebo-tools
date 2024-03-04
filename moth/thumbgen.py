"""
Generate thumbnails.
"""

import argparse
from pathlib import Path

from PIL import Image

THUMBNAIL_PREFIX = "thumbnail_"

THUMBNAILS = (
    (100, "1.png"),
    (200, "*.jpg"),
    (600, "*.jpg"),
)

parser = argparse.ArgumentParser(description=__doc__)


def main():
    parser.parse_args()

    for size, pattern in THUMBNAILS:
        for path in Path().rglob(pattern):
            if path.is_dir():
                continue

            if path.name.startswith(THUMBNAIL_PREFIX):
                continue

            dest_path = path.with_name(f"{THUMBNAIL_PREFIX}_{size}_{path.name}")
            if dest_path.exists():
                continue

            with Image.open(path) as im:
                im.thumbnail((size, size))
                im.save(dest_path)


if __name__ == "__main__":
    main()
