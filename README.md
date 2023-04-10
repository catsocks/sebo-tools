# Sebo wand

A command-line tool for organizing and processing photos, tailored to my very
particular use-case.

_Sebo_ stands for second-hand book store in Portuguese.

## Usage

```
Usage: wand [OPTIONS] FOLDER COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

  Commands for organizing and processing files that match '--suffix' in the
  given folder and its subfolders.

Options:
  --suffix TEXT  [default: .jpg, .jpeg, .png, .heic]
  --help         Show this message and exit.

Commands:
  count         Print the number of files in folders.
  create-cover  Generate the "product cover" version of images.
  mkdirs        Create a given number of directories.
  normalize     Normalize images.
  rename        Rename files using an ascending sequence of numbers.
```

For more details, have a look at [sebo_wand.py](sebo_wand.py) and
[test_sebo_wand.py](tests/test_sebo_wand.py).

## Develop

In case you're on Fedora Linux,
[Remi's RPM repository](https://rpms.remirepo.net/) provide HEIC support for
ImageMagick through the _ImageMagick-heic_ package.

## To do

* [ ] Add `--verbose` option.
* [ ] Use a simpler alternative to [rembg](https://github.com/danielgatis/rembg).
* [ ] Add command for grouping photos of the same object into folders.
* [ ] Add command for scraping the text contents of all the photos.

## My related projects

- [Sebo inventory](https://github.com/catsocks/sebo-inventory-gs) Google Apps Script project

## License

Read the [BSD-0](LICENSE.txt) license.
