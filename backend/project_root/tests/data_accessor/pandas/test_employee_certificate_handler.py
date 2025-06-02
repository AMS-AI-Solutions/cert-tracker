import pytest
from pathlib import Path
from datetime import date
import pandas as pd

from app.data_accessor.pandas.employee_certificate_handler import EmployeeCertificateHandler
from app.data_models.employee_certificate import EmployeeCertificate

@pytest.fixture
def employee_certificate_data():
    return [
        {"employee_id": 1, "course_id": "C001", "certificate_name": "Asbestos Abatement Techniques Certification", "certificate_id": "CERT001", "issue_date": "2023-01-01", "expiry_date": "2025-12-31"},
        {"employee_id": 2, "course_id": "C001", "certificate_name": "Asbestos Abatement Techniques Certification", "certificate_id": "CERT002", "issue_date": "2023-06-01", "expiry_date": "2024-06-30"},
        {"employee_id": 1, "course_id": "C003", "certificate_name": "Chainsaw Operation Certification", "certificate_id": "CERT003", "issue_date": "2022-12-01", "expiry_date": "2023-01-15"},
    ]

@pytest.fixture
def csv_file(tmp_path: Path, employee_certificate_data):
    df = pd.DataFrame(employee_certificate_data).set_index("employee_id")
    path = tmp_path / "employee_certificates.csv"
    df.to_csv(path)
    return path


def test_get_certificate_by_id_found(csv_file):
    handler = EmployeeCertificateHandler(csv_file)
    cert = handler.get_certificate_by_id("CERT002")
    assert isinstance(cert, EmployeeCertificate)
    assert cert.certificate_id == "CERT002"
    assert cert.employee_id == 2


def test_get_certificate_by_id_not_found(csv_file):
    handler = EmployeeCertificateHandler(csv_file)
    assert handler.get_certificate_by_id("NOT_EXIST") is None


def test_get_employee_certificates_by_employee_id(csv_file):
    handler = EmployeeCertificateHandler(csv_file)
    certs = handler.get_employee_certificates_by_employee_id(1)
    assert len(certs) == 2
    assert all(cert.employee_id == 1 for cert in certs)


def test_get_employee_certificates_by_course_id(csv_file):
    handler = EmployeeCertificateHandler(csv_file)
    certs = handler.get_employee_certificates_by_course_id("C001")
    assert len(certs) == 2
    assert all(cert.course_id == "C001" for cert in certs)


def test_get_expired_employee_certificates_by_date_range(csv_file):
    handler = EmployeeCertificateHandler(csv_file)
    expired = handler.get_certificates_expiring_in_time_range(
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31)
    )
    assert len(expired) == 1
    assert expired[0].certificate_id == "CERT003"



def test_get_certificates_expiring_within(csv_file):
    handler = EmployeeCertificateHandler(csv_file)
    certs = handler.get_certificates_expiring_within(30, from_date=date(2024, 6, 1))
    assert len(certs) == 1
    assert certs[0].certificate_id == "CERT002"


def test_count_and_group(csv_file):
    handler = EmployeeCertificateHandler(csv_file)
    counts_emp = handler.count_certificates_by_employee()
    assert counts_emp[1] == 2 and counts_emp[2] == 1
    groups_emp = handler.group_certificates_by_employee()
    assert set(groups_emp.keys()) == {1, 2}
    assert len(groups_emp[1]) == 2
    counts_course = handler.count_certificates_by_course()
    assert counts_course["C001"] == 2 and counts_course["C003"] == 1
    groups_course = handler.group_certificates_by_course()
    assert set(groups_course.keys()) == {"C001", "C003"}
    assert len(groups_course["C001"]) == 2


def test_find_by_certificate_name(csv_file):
    handler = EmployeeCertificateHandler(csv_file)
    results = handler.find_by_certificate_name("asbestos")
    assert len(results) == 2


