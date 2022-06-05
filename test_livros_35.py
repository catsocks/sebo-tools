from pathlib import Path

import pytest

from livros_35 import print_image_urls, rename_images


@pytest.fixture
def tmppath(tmpdir):
    return Path(tmpdir)


def test_print_image_urls(tmppath, capfd):
    folder = (tmppath / "some-book")
    folder.mkdir()

    (folder / "1.png").touch()
    (folder / "2.jpg").touch()

    print_image_urls(folder, "https://example.com")
    out, _ = capfd.readouterr()
    assert out == (
        f"https://example.com/{folder.name}/1.png "
        f"https://example.com/{folder.name}/2.jpg \n"
    )


def test_rename_images(tmppath):
    (tmppath / "20220605_084510.jpg").touch()
    (tmppath / "20220605_084511.jpg").touch()

    rename_images(tmppath, sequence_start=2)

    names = [path.name for path in sorted(tmppath.iterdir())]
    assert names == ["2.jpg", "3.jpg"]


# @pytest.mark.removebg
# def test_make_cover(tmppath):
#     pass
