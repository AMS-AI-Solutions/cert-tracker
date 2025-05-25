from typing import List
from datetime import date

from app.data_accessor.pandas.course_handler import CourseHandler
from app.data_accessor.pandas.employee_handler import EmployeeHandler
from app.data_models.employee_certificate import EmployeeCertificate
from app.data_accessor.pandas.employee_certificate_handler import EmployeeCertificateHandler

class CertTrackerService:
    def __init__(
        self,
        employee_cert_repo: EmployeeCertificateHandler,
        course_repo: CourseHandler,
        employee_repo: EmployeeHandler,
    ):
        self.employee_certs = employee_cert_repo.load_all()
        self.courses = {c.course_id: c for c in course_repo.load_all()}
        self.employees = {e.employee_id: e for e in employee_repo.load_all()}

    def get_expiring_certificates(self, start: date, end: date) -> List[EmployeeCertificate]:
        return [cert for cert in self.employee_certs if start <= cert.expiry_date <= end]