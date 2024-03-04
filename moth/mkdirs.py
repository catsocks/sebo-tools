"""
Create a given number of directories named with an ascending sequence of
numbers.
"""

import argparse
import os

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "start", type=int, help="the number from which to start the sequence"
)
parser.add_argument("count", type=int, help="the number of directories to create")


def main():
    args = parser.parse_args()

    for n in range(args.start, args.start + args.count):
        try:
            os.mkdir(str(n))
        except FileExistsError:
            pass


if __name__ == "__main__":
    main()
