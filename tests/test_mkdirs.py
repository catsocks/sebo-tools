from click.testing import CliRunner

from sebo_tools.mkdirs import cli


def test_mkdirs(data_path, monkeypatch):
    monkeypatch.chdir(data_path)

    runner = CliRunner()
    result = runner.invoke(cli, ["2"])
    assert result.exit_code == 0
    assert (data_path / "1").exists()
    assert (data_path / "2").exists()

    result = runner.invoke(cli, ["2"])
    assert result.exit_code == 0
    assert (data_path / "3").exists()
    assert (data_path / "4").exists()

    result = runner.invoke(cli, ["2", "--start-from", "9"])
    assert result.exit_code == 0
    assert (data_path / "9").exists()
    assert (data_path / "10").exists()

    result = runner.invoke(cli, ["2", "--start-from", "1"])
    assert result.exit_code == 0
