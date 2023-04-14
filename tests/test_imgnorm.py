from click.testing import CliRunner

from sebo_tools.imgnorm import cli


def test_imgnorm(data_path):
    runner = CliRunner()
    book_path = data_path / "book-b"
    result = runner.invoke(cli, [str(book_path)])
    assert result.exit_code == 0
    assert next(book_path.glob("*.jpeg"), None) is None
    assert next(book_path.glob("*.heic"), None) is None
