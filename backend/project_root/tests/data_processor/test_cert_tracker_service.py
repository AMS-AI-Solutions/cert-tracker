# tests/test_cert_tracker_service.py
import pytest
from datetime import date, timedelta

from app.data_models.employee_certificate import EmployeeCertificate
from app.data_accessor.employee_certificate_handler import EmployeeCertificateHandler
from app.data_accessor.course_handler import CourseHandler
from app.data_accessor.employee_handler import EmployeeHandler
from app.data_processor.cert_tracker_service import CertTrackerService


# --- Helpers / Mocks ---

class DummyCourse:
    def __init__(self, course_id, name=""):
        self.course_id = course_id
        self.name = name

class DummyEmployee:
    def __init__(self, employee_id, name=""):
        self.employee_id = employee_id
        self.name = name

class FakeCourseRepo(CourseHandler):
    def load_all(self):
        # Return two dummy courses
        return [DummyCourse(course_id=1), DummyCourse(course_id=2)]

class FakeEmployeeRepo(EmployeeHandler):
    def load_all(self):
        # Return two dummy employees
        return [DummyEmployee(employee_id=10), DummyEmployee(employee_id=20)]

class FakeCertRepo(EmployeeCertificateHandler):
    def __init__(self, certs):
        self._certs = certs

    def load_all(self):
        return self._certs

# --- Fixtures ---

@pytest.fixture
def today():
    return date.today()

@pytest.fixture
def certs(today):
    # create certificates expiring yesterday, today, in 3 days, and in 10 days
    return [
        EmployeeCertificate(employee_id=10, course_id=1,
                            issue_date=today - timedelta(days=365),
                            expiry_date=today - timedelta(days=1)),
        EmployeeCertificate(employee_id=10, course_id=1,
                            issue_date=today - timedelta(days=200),
                            expiry_date=today),
        EmployeeCertificate(employee_id=20, course_id=2,
                            issue_date=today - timedelta(days=100),
                            expiry_date=today + timedelta(days=3)),
        EmployeeCertificate(employee_id=20, course_id=2,
                            issue_date=today - timedelta(days=50),
                            expiry_date=today + timedelta(days=10)),
    ]

@pytest.fixture
def service(certs):
    fake_cert_repo = FakeCertRepo(certs)
    fake_course_repo = FakeCourseRepo()
    fake_employee_repo = FakeEmployeeRepo()
    return CertTrackerService(
        employee_cert_repo=fake_cert_repo,
        course_repo=fake_course_repo,
        employee_repo=fake_employee_repo,
    )

# --- Tests ---

def test_get_expiring_within_range_includes_boundaries(service, today):
    start = today - timedelta(days=0)     # today
    end   = today + timedelta(days=3)     # in 3 days

    results = service.get_expiring_certificates(start, end)
    # should include the cert expiring today and in 3 days, exclude yesterday and in 10 days
    expiries = {c.expiry_date for c in results}
    assert today in expiries
    assert today + timedelta(days=3) in expiries
    assert today - timedelta(days=1) not in expiries
    assert today + timedelta(days=10) not in expiries
    assert len(results) == 2

def test_get_expiring_no_matches(service, today):
    # choose a window outside any expiry dates
    start = today + timedelta(days=20)
    end   = today + timedelta(days=30)
    results = service.get_expiring_certificates(start, end)
    assert results == []

def test_get_expiring_full_range_returns_all_in_range(service, today):
    # choose a wide range that covers everything except the past one
    start = today - timedelta(days=2)
    end   = today + timedelta(days=15)
    results = service.get_expiring_certificates(start, end)
    # only the first certificate (expired yesterday) is out of range
    assert all(start <= c.expiry_date <= end for c in results)
    assert len(results) == 3
