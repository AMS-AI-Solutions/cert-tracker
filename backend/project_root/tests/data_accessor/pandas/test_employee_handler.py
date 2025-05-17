import pytest
from pathlib import Path
import pandas as pd

from app.data_accessor.pandas.employee_handler import EmployeeHandler
from app.data_models.employee import Employee

@pytest.fixture
def employee_data():
    # Only include fields defined on Employee model
    return [
        {
            "employee_id": 1,
            "first_name": "Alice",
            "last_name": "Smith",
            "company_name": "Acme Corp",
            "department": "Sales",
            "email": "alice.smith@acme.com",
        },
        {
            "employee_id": 2,
            "first_name": "Bob",
            "last_name": "Brown",
            "company_name": "Initech",
            "department": "Engineering",
            "email": "bob.brown@initech.com",
        },
        {
            "employee_id": 3,
            "first_name": "Cara",
            "last_name": "Davis",
            "company_name": "Hooli",
            "department": "HR",
            "email": "cara.davis@hooli.com",
        },
    ]

@pytest.fixture
def csv_file(tmp_path: Path, employee_data):
    # Create a CSV matching the Employee model fields, index on employee_id
    df = pd.DataFrame(employee_data).set_index("employee_id")
    path = tmp_path / "employees.csv"
    df.to_csv(path)
    return path


def test_get_by_id_exists(csv_file):
    repo = EmployeeHandler(csv_file)
    emp = repo.get_by_id(2)

    assert isinstance(emp, Employee)
    assert emp.employee_id == 2
    assert emp.first_name == "Bob"
    assert emp.last_name == "Brown"
    assert emp.company_name == "Initech"
    assert emp.department == "Engineering"
    assert emp.email == "bob.brown@initech.com"


def test_get_by_id_not_exists(csv_file):
    repo = EmployeeHandler(csv_file)
    assert repo.get_by_id(999) is None


def test_get_company_name_from_employee_name_exact(csv_file):
    repo = EmployeeHandler(csv_file)
    # Should return the company_name for the matched employee
    assert repo.get_company_name_from_employee_name("Alice Smith") == "Acme Corp"


def test_get_company_name_from_employee_name_case_insensitive(csv_file):
    repo = EmployeeHandler(csv_file)
    assert repo.get_company_name_from_employee_name("alice smith") == "Acme Corp"
    assert repo.get_company_name_from_employee_name("ALICE SMITH") == "Acme Corp"


def test_get_company_name_not_exists(csv_file):
    repo = EmployeeHandler(csv_file)
    assert repo.get_company_name_from_employee_name("Nonexistent Person") is None
