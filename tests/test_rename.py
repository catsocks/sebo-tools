from click.testing import CliRunner

from sebo_tools.rename import cli


def test_rename(data_path):
    runner = CliRunner()
    result = runner.invoke(cli, [str(data_path)])
    assert result.exit_code == 0
    assert (data_path / "book-a" / "2.jpg").exists()
    assert (data_path / "book-a" / "book-d" / "2.jpg").exists()
    assert (data_path / "book-b" / "2.jpeg").exists()
    assert (data_path / "book-b" / "3.jpg").exists()
    assert (data_path / "book-b" / "4.heic").exists()
