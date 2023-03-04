from pathlib import Path

import pytest
from click.testing import CliRunner
from numba.core.config import shutil

from sebo_magic import cli


@pytest.fixture()
def data_path(tmp_path):
    shutil.copytree(Path("tests/data"), tmp_path, dirs_exist_ok=True)
    return tmp_path


def test_cli_no_args():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_rename_images(data_path):
    runner = CliRunner()
    result = runner.invoke(cli, [str(data_path), "rename-files"])
    assert result.exit_code == 0
    assert (data_path / "book-a" / "2.jpg").exists()
    assert (data_path / "book-a" / "book-d" / "2.jpg").exists()
    assert (data_path / "book-a" / "book-d" / ".DS_Store").exists()
    assert (data_path / "book-b" / "2.jpg").exists()
    assert (data_path / "book-b" / "3.heic").exists()


def test_normalize_images(data_path):
    runner = CliRunner()
    book_path = data_path / "book-b"
    result = runner.invoke(cli, [str(book_path), "normalize-images"])
    assert result.exit_code == 0
    assert (book_path / "3.jpg").exists()


def test_create_cover_images(data_path):
    runner = CliRunner()
    book_path = data_path / "book-b"
    result = runner.invoke(cli, [str(book_path), "create-cover-images"])
    assert result.exit_code == 0
    assert (book_path / "1.png").exists()


def test_count_files(data_path):
    runner = CliRunner()
    result = runner.invoke(cli, [str(data_path), "count-files"])
    assert result.exit_code == 0
    assert result.output == ("book-a\t1\n" "book-a\\book-d\t1\n" "book-b\t2\n")


def test_all_chained(data_path):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            str(data_path),
            "rename-files",
            "normalize-images",
            "create-cover-images",
            "count-files",
        ],
    )
    assert result.exit_code == 0
    assert (data_path / "book-a" / "1.png").exists()
    assert (data_path / "book-a" / "2.jpg").exists()
    assert (data_path / "book-a" / "book-d" / "1.png").exists()
    assert (data_path / "book-a" / "book-d" / "2.jpg").exists()
    assert (data_path / "book-b" / "1.png").exists()
    assert (data_path / "book-b" / "2.jpg").exists()
    assert (data_path / "book-b" / "3.jpg").exists()
