# Sebo Magic

A collection of small tools to help me manage the process of taking photos of
products.

_Sebo_ stands for second-hand book shop in Portuguese.

## Use case

Assuming you've taken photos of many products, grouped them into folders, and want to mass-upload them to your store, this tool can help you with the following commands:

| Command | Description |
| --- | --- |
| rename | Rename the photos using a sequence of numbers based on the natural sort order of their filenames. |
| normalize | Normalize the format, maximum resolution, and rotation of the photos. |
| create-cover | Automatically create a product cover photo based off of an image from each folder. |
| count | Print the number of photos in each folder in a spreadsheet-friendly way (i.e. using tab separated values). |

For more details, have a look at [sebo_magic.py](sebo_magic.py) and [test_sebo_magic.py](tests/test_sebo_magic.py).

## Usage

```
Usage: magic [OPTIONS] FOLDER COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

  A set of commands that processes files matching the given suffixes in a
  given folder tree.

Options:
  --suffixes TEXT  [default: .jpg, .png, .heic]
  --help           Show this message and exit.

Commands:
  count         Print the number of files for each folder.
  create-cover  Remove the background of, and resize if necessary, the...
  normalize     Normalize the format, maximum resolution, and rotation of...
  rename        Rename the files using a sequence of numbers based on the...
```

## TODO

* [ ] Add `--verbose` option.
* [ ] Use a simpler alternative to [rembg](https://github.com/danielgatis/rembg).
* [ ] Add command for grouping photos of the same object into folders.
* [ ] Add command for scraping the text contents of all the photos.

## License

Read the [BSD-0](LICENSE.txt) license.
