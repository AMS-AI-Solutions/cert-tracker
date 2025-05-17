import pytest
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import Optional
from pydantic import BaseModel

from app.data_accessor.pandas.pandas_handler import PandasHandler

class User(BaseModel):
    id: int
    name: str
    signup_date: Optional[datetime] = None

@pytest.fixture
def sample_data():
    return [
        {"id": 1, "name": "Alice", "signup_date": "2025-01-01"},
        {"id": 2, "name": "Bob",   "signup_date": "2025-02-15"},
        {"id": 3, "name": "Cara",  "signup_date": "2025-03-30"},
    ]

@pytest.fixture
def csv_file(tmp_path: Path, sample_data):
    df = pd.DataFrame(sample_data)
    path = tmp_path / "users.csv"
    df.to_csv(path, index=False)
    return path

def test_load_all_basic(csv_file, sample_data):
    handler = PandasHandler(csv_file, User)
    users = handler.load_all()

    assert len(users) == len(sample_data)
    for original, loaded in zip(sample_data, users):
        # Pydantic will parse the ISO-8601 strings into datetime:
        assert isinstance(loaded.signup_date, datetime)
        assert loaded.signup_date == datetime.fromisoformat(original["signup_date"])

def test_load_all_with_parse_dates(csv_file, sample_data):
    handler = PandasHandler(csv_file, User, parse_dates=["signup_date"])
    users = handler.load_all()
    for loaded in users:
        assert isinstance(loaded.signup_date, datetime)
    assert users[0].signup_date == datetime(2025, 1, 1)
    assert users[1].signup_date == datetime(2025, 2, 15)
    assert users[2].signup_date == datetime(2025, 3, 30)

def test_load_all_with_index_col(tmp_path: Path, sample_data):
    # write CSV with id as index
    df = pd.DataFrame(sample_data).set_index("id")
    path = tmp_path / "users_indexed.csv"
    df.to_csv(path)

    handler = PandasHandler(path, User, parse_dates=["signup_date"], index_col="id")
    users = handler.load_all()

    assert {u.id for u in users} == {1, 2, 3}
    assert all(isinstance(u.signup_date, datetime) for u in users)
