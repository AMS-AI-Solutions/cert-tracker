import pytest
import tempfile
from typing import Generator
from pathlib import Path
from textwrap import dedent
from datetime import date

from app.data_accessor.employee_certificate_handler import EmployeeCertificateHandler

@pytest.fixture
def employee_certificate_csv_file() -> Generator[Path, None, None]:
    content = dedent("""\
        employee_id,course_id,certificate_name,issue_date,expiry_date
        1,c-111,Asbestos Abatement Techniques Certification,2022-12-16,2025-12-16
        2,c-222,Chainsaw Operation Certification,2021-10-19,2025-10-19
    """)
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".csv") as tmp:
        tmp.write(content)
        tmp.flush()
        yield Path(tmp.name)
        tmp.close()


def test_load_all(employee_certificate_csv_file):
    handler = EmployeeCertificateHandler(employee_certificate_csv_file)
    certificates = handler.load_all()

    assert len(certificates) == 2
    assert certificates[0].certificate_name == "Asbestos Abatement Techniques Certification"
    assert certificates[1].issue_date == date(2021, 10, 19)



def test_get_expired_employee_certificates_by_date_range(employee_certificate_csv_file):
    handler = EmployeeCertificateHandler(employee_certificate_csv_file)
    expired_certificates = handler.get_expired_employee_certificates_by_date_range(
        date(2025, 10, 1), date(2025, 10, 20)
    )

    assert len(expired_certificates) == 1
    assert expired_certificates[0].certificate_name == "Chainsaw Operation Certification"
    assert expired_certificates[0].issue_date == date(2021, 10, 19)

def test_get_employee_certificates_by_employee_id(employee_certificate_csv_file):
    handler = EmployeeCertificateHandler(employee_certificate_csv_file)
    certificates = handler.get_employee_certificates_by_employee_id(1)

    assert len(certificates) == 1
    assert certificates[0].certificate_name == "Asbestos Abatement Techniques Certification"
    assert certificates[0].issue_date == date(2022, 12, 16)

def test_get_employee_certificates_by_employee_id_not_found(employee_certificate_csv_file):
    handler = EmployeeCertificateHandler(employee_certificate_csv_file)
    certificates = handler.get_employee_certificates_by_employee_id(3)

    assert len(certificates) == 0

def test_get_employee_certificates_by_course_id(employee_certificate_csv_file):
    handler = EmployeeCertificateHandler(employee_certificate_csv_file)
    certificates = handler.get_employee_certificates_by_course_id('c-111')

    assert len(certificates) == 1
    assert certificates[0].certificate_name == "Asbestos Abatement Techniques Certification"
    