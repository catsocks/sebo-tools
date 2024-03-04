"""
Count the number of files in folders.
"""

import argparse
from pathlib import Path

from natsort import natsorted

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "pattern",
    nargs="?",
    default="*",
    help="recursive glob pattern (e.g.: '[!thumbnail_]*' to exclude files that begin with \"thumbnail_\")",
)
parser.add_argument(
    "--full", action="store_true", help="full output", dest="full_output"
)


def print_count(working_directory, directory, count, full_output):
    if not full_output:
        print(count)
        return

    relative_path = directory.relative_to(working_directory).as_posix()
    print(f"{relative_path}\t{count}")


def main():
    args = parser.parse_args()

    wd = Path()

    path = None
    current_parent = None
    current_count = 0
    for path in natsorted(wd.rglob(args.pattern)):
        if path.is_dir():
            continue

        if current_parent != path.parent:
            if current_parent is not None:
                print_count(wd, current_parent, current_count, args.full_output)

            current_parent = path.parent
            current_count = 0

        current_count += 1

    if path:
        print_count(wd, current_parent, current_count, args.full_output)


if __name__ == "__main__":
    main()
