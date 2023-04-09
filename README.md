# Sebo wand

A command-line tool for processing photos, tailored to my very particular
use-case.

_Sebo_ stands for second-hand book store in Portuguese.

## Usage

```
Usage: wand [OPTIONS] FOLDER COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

  A set of commands that processes files matching the given suffixes in a
  given folder tree.

Options:
  --suffixes TEXT  [default: .jpg, .jpeg, .png, .heic]
  --help           Show this message and exit.

Commands:
  count         Print the number of files for each folder.
  create-cover  Remove the background of, and resize if necessary, the...
  normalize     Normalize the format, maximum resolution, and rotation of...
  rename        Rename the files using a sequence of numbers based on the...
```

For more details, have a look at [sebo_wand.py](sebo_wand.py) and
[test_sebo_wand.py](tests/test_sebo_wand.py).

## To do

* [ ] Add `--verbose` option.
* [ ] Use a simpler alternative to [rembg](https://github.com/danielgatis/rembg).
* [ ] Add command for grouping photos of the same object into folders.
* [ ] Add command for scraping the text contents of all the photos.

## My related projects

- [Sebo inventory](https://github.com/catsocks/sebo-inventory-gs) Google Apps Script

## License

Read the [BSD-0](LICENSE.txt) license.
