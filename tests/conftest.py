import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def data_path(tmp_path):
    shutil.copytree(Path("tests/data"), tmp_path, dirs_exist_ok=True)
    return tmp_path
