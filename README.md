# Sebo Magic

A collection of small tools for managing photos of products.

_Sebo_ stands for second-hand book shop in Portuguese.

## Use case

Assuming you've taken photos of many products, grouped them into folders, and want to mass-upload them to your store, this tool can help you with the following commands:

| Command | Description |
| --- | --- |
| rename-files | Rename the photos according to the lexographical order of their filenames in each folder. |
| normalize-images | Normalize the format, maximum resolution, and rotation of the photos. |
| create-cover-images | Automatically create a product cover photo based off an image from each folder. |
| count-files | Print the number of photos in each folder in a spreadsheet-friendly way (i.e. using tab separated values). |

All the commands above work recursively on a folder tree.

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
  count-files          Print the number of files that match the given...
  create-cover-images  Remove the background of, and resize if necessary,...
  normalize-images     Normalize the format, maximum resolution, and...
  rename-files         Rename files according to the lexographical order...
```

## TODO

* [ ] Use natural sort order for sorting files.
* [ ] Add `--verbose` option.
* [ ] Use a simpler alternative to [rembg](https://github.com/danielgatis/rembg).
* [ ] Add command for grouping photos of the same object into folders.
* [ ] Add command for scraping the text contents of all the photos.

## License

Read the [BSD-0](LICENSE.txt) license.
