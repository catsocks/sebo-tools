"""
Generate product cover images.

Covers are generated using remove.bg's paid API for background removal that comes with
some free credits.
"""

# NOTES(catsocks): I would like to add an option for local background removal, using a
# package like danielgatis/rembg, but its built-in models do not work well with the
# photos I take, and I have yet to try fine-tuning one of them.

import argparse
import io
import logging
import os
from pathlib import Path

import requests  # simpler than brilam/remove-bg.
from PIL import Image, ImageOps

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--api-key",
    default=os.environ.get("MOTH_COVERGEN_API_KEY"),
    help="(default: $MOTH_COVERGEN_API_KEY)",
)


def main():
    logging.getLogger().setLevel(logging.INFO)

    args = parser.parse_args()

    for path in Path().rglob("2.jpg"):
        new_path = path.with_name("1.png")
        if new_path.exists():
            logging.info(f"{path} exists, skipping")
            continue

        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": path.read_bytes()},
            data={
                "size": "auto",
                "type": "product",
            },
            headers={"X-Api-Key": args.api_key},
        )
        if response.status_code != requests.codes.ok:
            logging.error(f"{path}: remove.bg: {response.text}")
            continue

        with Image.open(io.BytesIO(response.content)) as im:
            # Preferred image size in the Mercado Livre platform.
            im = ImageOps.cover(im, (1200, 1200))
            im.save(new_path)


if __name__ == "__main__":
    main()
