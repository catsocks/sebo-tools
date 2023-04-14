from click.testing import CliRunner

from sebo_tools.count import cli


def test_count(data_path):
    runner = CliRunner()
    result = runner.invoke(cli, [str(data_path)])
    assert result.exit_code == 0
    assert "book-a\t1\n" in result.output
    assert "book-a/book-d\t1\n" in result.output
    assert "book-b\t3\n" in result.output
