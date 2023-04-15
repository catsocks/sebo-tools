import os
import pytest
from click.testing import CliRunner


from sebo_tools.covergen import cli


def test_covergen_using_rembg(data_path):
    pytest.importorskip("rembg")

    runner = CliRunner()
    book_path = data_path / "book-b"
    result = runner.invoke(cli, ["--use-rembg", str(book_path)])
    assert result.exit_code == 0
    assert (book_path / "1.png").exists()


def test_covergen_using_remove_bg(data_path):
    envvar = "REMOVE_BG_API_KEY"
    if os.getenv(envvar) is None:
        pytest.skip(f"Please set the environment variable {envvar} to test the "
            + "remove.bg API.")

    runner = CliRunner()
    book_path = data_path / "book-b"
    result = runner.invoke(cli, ["--use-remove-bg", str(book_path)])
    assert result.exit_code == 0
    assert (book_path / "1.png").exists()

