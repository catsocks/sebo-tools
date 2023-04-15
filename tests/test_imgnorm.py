from click.testing import CliRunner
import wand.image
from wand.image import ORIENTATION_TYPES, Image

from sebo_tools.imgnorm import cli


def test_imgnorm(data_path):
    runner = CliRunner()
    book_path = data_path / "book-b"
    result = runner.invoke(cli, [str(book_path)])
    assert result.exit_code == 0
    assert next(book_path.glob("*.jpeg"), None) is None
    assert next(book_path.glob("*.heic"), None) is None


def test_auto_orientation(data_path):
    runner = CliRunner()
    book_path = data_path / "book-b"
    
    with Image(filename=book_path / "1.jpeg") as img:
        assert img.orientation == "right_top"

    result = runner.invoke(cli, [str(book_path)])
    assert result.exit_code == 0

    with Image(filename=book_path / "1.jpg") as img:
        assert img.orientation == "top_left"

