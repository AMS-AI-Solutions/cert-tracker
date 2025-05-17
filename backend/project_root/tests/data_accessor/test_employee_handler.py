import pytest
import tempfile
from pathlib import Path
from textwrap import dedent
from typing import Generator

from app.data_models.employee import Employee
from app.data_accessor.csv_handler import CsvHandler
from app.data_accessor.employee_handler import EmployeeHandler


@pytest.fixture
def employee_csv_file() -> Generator[Path, None, None]:
    content = dedent("""\
        employee_id,first_name,last_name,company_name,department,email
        1,John,Doe,OpenAI,Engineering,john.doe@example.com
        2,Jane,Smith,Google,Marketing,jane.smith@example.com
    """)
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".csv") as tmp:
        tmp.write(content)
        tmp.flush()
        yield Path(tmp.name)
        tmp.close()


def test_load_all(employee_csv_file):
    handler = EmployeeHandler(employee_csv_file)
    employees = handler.load_all()

    assert len(employees) == 2
    assert employees[0].first_name == "John"
    assert employees[1].last_name == "Smith"


def test_get_by_id(employee_csv_file):
    handler = EmployeeHandler(employee_csv_file)
    employee = handler.get_by_id(2)

    assert employee is not None
    assert employee.first_name == "Jane"
    assert employee.email == "jane.smith@example.com"


def test_get_employee_company_name(employee_csv_file):
    handler = EmployeeHandler(employee_csv_file)
    company_name = handler.get_employee_company_name("John", "Doe")

    assert company_name == "OpenAI"


def test_get_employee_email(employee_csv_file):
    handler = EmployeeHandler(employee_csv_file)
    email = handler.get_employee_email("Jane", "Smith")

    assert email == "jane.smith@example.com"


def test_cache_behavior(employee_csv_file, mocker):
    handler = EmployeeHandler(employee_csv_file)

    # Spy on the parent's load_all
    spy = mocker.spy(CsvHandler, 'load_all')

    handler.load_all()
    handler.load_all()  # should use cache on second call

    assert spy.call_count == 1
