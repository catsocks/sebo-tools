import pytest
from click.testing import CliRunner


from sebo_tools.covergen import cli


def test_covergen_with_rembg(data_path):
    pytest.importorskip("rembg")

    runner = CliRunner()
    book_path = data_path / "book-b"
    result = runner.invoke(cli, ["--use-rembg", str(book_path)])
    assert result.exit_code == 0
    assert (book_path / "1.png").exists()
