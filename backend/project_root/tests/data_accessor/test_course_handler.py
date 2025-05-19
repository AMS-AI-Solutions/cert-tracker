import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from app.data_accessor.pandas.course_handler import CourseHandler
from app.data_models.course import Course
import pandas as pd
from pathlib import Path

@pytest.fixture
def mock_course_handler():
    mock_df = pd.DataFrame([
        {"course_name": "Data Science Basics", "certificate_name": "Intro to DS Certificate"},
        {"course_name": "Python Programming", "certificate_name": "Python Cert"}
    ], index=["C001", "C002"])

    # Patch __init__ to do nothing
    with patch.object(CourseHandler, "__init__", lambda x, y: None):
        handler = CourseHandler(Path("dummy.csv"))
        handler.df = mock_df
        return handler


def test_get_by_id_found(mock_course_handler):
    result = mock_course_handler.get_by_id("C001")
    assert isinstance(result, Course)
    assert result.course_id == "C001"
    assert result.course_name == "Data Science Basics"
    assert result.certificate_name == "Intro to DS Certificate"


def test_get_by_id_not_found(mock_course_handler):
    result = mock_course_handler.get_by_id("C999")
    assert result is None


def test_get_by_course_name_from_certificate_name_found(mock_course_handler):
    result = mock_course_handler.get_by_course_name_from_certificate_name("Python Cert")
    assert result == "Python Programming"


def test_get_by_course_name_from_certificate_name_not_found(mock_course_handler):
    result = mock_course_handler.get_by_course_name_from_certificate_name("Nonexistent Cert")
    assert result is None
