"""
Rename files using an ascending number sequence.
"""

import argparse
import logging
from pathlib import Path

from natsort import natsorted

SEQUENCE_START = 2

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("pattern", nargs="?", default="*", help="recursive glob pattern")


def main():
    logging.getLogger().setLevel(logging.INFO)

    args = parser.parse_args()

    current_index = SEQUENCE_START
    current_parent = None

    for path in natsorted(Path().rglob(args.pattern)):
        if path.is_dir():
            continue

        if path.parent != current_parent:
            current_index = SEQUENCE_START
            current_parent = path.parent

        new_path = path.with_stem(str(current_index))
        if new_path.exists():
            logging.info(f"{new_path} already exists, skipping")
        else:
            path.replace(new_path)

        current_index += 1


if __name__ == "__main__":
    main()
