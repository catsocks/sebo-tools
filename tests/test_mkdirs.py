from click.testing import CliRunner

from sebo_tools.mkdirs import cli


def test_mkdirs(data_path):
    runner = CliRunner()
    result = runner.invoke(cli, [str(data_path), "2"])
    assert result.exit_code == 0
    assert (data_path / "1").exists()
    assert (data_path / "2").exists()
