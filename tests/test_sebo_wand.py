from pathlib import Path

import pytest
from click.testing import CliRunner
import shutil

from sebo_wand import cli


@pytest.fixture()
def data_path(tmp_path):
    shutil.copytree(Path("tests/data"), tmp_path, dirs_exist_ok=True)
    return tmp_path


def test_cli_no_args():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_rename(data_path):
    runner = CliRunner()
    result = runner.invoke(cli, [str(data_path), "rename"])
    assert result.exit_code == 0
    assert (data_path / "book-a" / "2.jpg").exists()
    assert (data_path / "book-a" / "book-d" / "2.jpg").exists()
    assert (data_path / "book-a" / "book-d" / "Cake recipe.txt").exists()
    assert (data_path / "book-b" / "2.jpg").exists()
    assert (data_path / "book-b" / "3.jpeg").exists()
    assert (data_path / "book-b" / "4.heic").exists()


def test_normalize(data_path):
    runner = CliRunner()
    book_path = data_path / "book-b"
    result = runner.invoke(cli, [str(book_path), "normalize"])
    assert result.exit_code == 0
    assert next(book_path.glob("*.jpeg"), None) is None
    assert next(book_path.glob("*.heic"), None) is None


def test_create_cover(data_path):
    runner = CliRunner()
    book_path = data_path / "book-b"
    result = runner.invoke(cli, [str(book_path), "create-cover"])
    assert result.exit_code == 0
    assert (book_path / "1.png").exists()


def test_count(data_path):
    runner = CliRunner()
    result = runner.invoke(cli, [str(data_path), "count"])
    assert result.exit_code == 0
    assert "book-a\t1\n" in result.output
    assert "book-a/book-d\t1\n" in result.output
    assert "book-b\t3\n" in result.output


def test_mkdirs(data_path):
    runner = CliRunner()
    result = runner.invoke(cli, [str(data_path), "mkdirs", "2"])
    assert result.exit_code == 0
    assert (data_path / "1").exists()
    assert (data_path / "2").exists()


def test_all_chained(data_path):
    runner = CliRunner()
    result = runner.invoke(
        cli, [str(data_path), "rename", "normalize", "create-cover", "count"]
    )
    assert result.exit_code == 0
    assert (data_path / "book-a" / "1.png").exists()
    assert (data_path / "book-a" / "2.jpg").exists()
    assert (data_path / "book-a" / "book-d" / "1.png").exists()
    assert (data_path / "book-a" / "book-d" / "2.jpg").exists()
    assert (data_path / "book-b" / "1.png").exists()
    assert (data_path / "book-b" / "2.jpg").exists()
    assert (data_path / "book-b" / "3.jpg").exists()
    assert (data_path / "book-b" / "4.jpg").exists()
