import pytest
import tempfile
from pathlib import Path
from textwrap import dedent
from typing import Generator
from pydantic import BaseModel

from app.data_accessor.csv_handler import CsvHandler


class DummyModel(BaseModel):
    id: int
    name: str


@pytest.fixture
def dummy_csv_file() -> Generator[Path, None, None]:
    content = dedent("""\
        id,name
        1,Alice
        2,Bob
    """)
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as tmp:
        tmp.write(content)
        tmp.flush()
        yield Path(tmp.name)


def test_csv_handler_load_all(dummy_csv_file):
    handler = CsvHandler(dummy_csv_file, DummyModel)
    result = handler.load_all()

    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "Alice"
    assert result[1].id == 2
    assert result[1].name == "Bob"
