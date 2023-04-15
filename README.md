# Sebo tools

A package of command-line tools for organizing and processing photos, tailored
to my very particular use case.

_Sebo_ stands for second hand book store in Portuguese.

## Summary

- _sebo-mkdirs_ — Create a given number of folders.
- _sebo-rename_ — Rename files using an ascending sequence of numbers.
- _sebo-imgnorm_ — Normalize images in place.
- _sebo-covergen_ — Generate product cover images.
- _sebo-count_ — Count the number of files in folders.

The tools are listed in the order which I would normally use them.

## Usage

### sebo-mkdirs

```
Usage: sebo-mkdirs [OPTIONS] FOLDER NUMBER

  Create a given number of folders.

  The folders will be named using an ascending sequence of numbers starting
  from 1 or '--sequence-start' or the greatest integer used as the name of a
  subfolder.

Options:
  --sequence-start INTEGER
  --help                    Show this message and exit.
```

### sebo-rename

```
Usage: sebo-rename [OPTIONS] [FOLDER]

  Rename files using an ascending sequence of numbers.

  Applies to both the given folder and its subfolders.

  The order in which the files are named is determined by their natural sort
  order within their parent folder.

  The sequence is reset for every folder and begins with the value specified
  by '--sequence-start'.

Options:
  -v, --verbose
  --no-recursive
  --dry-run
  --sequence-start INTEGER  [default: 2]
  --help                    Show this message and exit.
```

### sebo-imgnorm

```
Usage: sebo-imgnorm [OPTIONS] [FOLDER]

  Normalize images in place.

  Normalize the file extension, format, maximum resolution, and orientation of
  images at the given folder and subfolders.

  If an image does not need to be normalized, the function will not overwrite
  it unless the '--force' flag is set.

Options:
  --no-recursive
  -f, --force
  -v, --verbose
  --dry-run
  --format TEXT          Image format.  [default: jpg]
  --extension TEXT       File extension.  [default: jpg]
  --max-resolution TEXT  [default: 1920x1920]
  --help                 Show this message and exit.
```

### sebo-covergen

```
Usage: sebo-covergen [OPTIONS] [FOLDER] COMMAND [ARGS]...

  Generate product cover images.

  Search for images that match '--input' at the given folder and subfolders.

  For each matching image, the background is removed, it is scaled down if
  necessary to fit '--max-resolution', and then it is saved to '--output'.

  The output file will not be overwriten unless the '--force' flag is set.

Options:
  --no-recursive
  -f, --force
  -v, --verbose
  --dry-run
  -i, --input TEXT          [default: 2.jpg]
  -o, --output TEXT         [default: 1.png]
  --max-resolution TEXT     [default: 1920x1920]
  --use-remove-bg
  --use-rembg
  --remove-bg-api-key TEXT
  --help                    Show this message and exit.
```

### sebo-count

```
Usage: sebo-count [OPTIONS] [FOLDER]

  Count the number of files in folders.

  The number of files at the given folder and subfolders will be printed beside
  their path relative to the given folder.

Options:
  --no-recursive
  --separator TEXT
  --help            Show this message and exit.
```

## Install

### Requirements

- Python 3.10

The _covergen_ tool will use the remove.bg paid API — which comes with some
"Free Previews" — by default, and it requires an account:

- [remove.bg](https://www.remove.bg/r/mYdNF6r5sTTkcp5zYn8Utz5G) API key

Alternatively, make sure to install this package with the free and offline
background remover [_rembg_](https://github.com/danielgatis/rembg) and pass the
flag `--use-rembg` to _covergen_.

I've made _rembg_ optional due to installation and performance issues.

#### Development

- [Poetry](https://python-poetry.org/) dependency manager

### Install as an user

Install this package into an isolated environment using
[pipx](https://pypa.github.io/pipx/):

    pipx install .[rembg]

Alternatively, use pip:

    pip install .[rembg]

The tools should now be available with their sebo-prefixed names.

### Install as a developer

Install this package with all optional dependencies into a virtual environment:

    poetry install --all-extras

Alternatively, omit `--all-extras` in case you run into issues installing
_rembg_.

## License

Read the [BSD-0](LICENSE.txt) license.
