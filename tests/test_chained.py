import pytest
from click.testing import CliRunner

from sebo_tools import covergen, imgnorm, rename


@pytest.mark.order("last")
def test_chain(data_path):
    pytest.importorskip("rembg")

    runner = CliRunner()
    runner.invoke(rename.cli, [str(data_path)])
    runner.invoke(imgnorm.cli, [str(data_path)])
    runner.invoke(covergen.cli, ["--use-rembg", str(data_path)])

    assert (data_path / "book-a" / "1.png").exists()
    assert (data_path / "book-a" / "2.jpg").exists()
    assert (data_path / "book-a" / "book-d" / "1.png").exists()
    assert (data_path / "book-a" / "book-d" / "2.jpg").exists()
    assert (data_path / "book-b" / "1.png").exists()
    assert (data_path / "book-b" / "2.jpg").exists()
    assert (data_path / "book-b" / "3.jpg").exists()
    assert (data_path / "book-b" / "4.jpg").exists()
