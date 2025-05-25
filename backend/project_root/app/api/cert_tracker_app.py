from pathlib import Path
from fastapi import FastAPI

from app.data_models.course import Course
from app.data_models.company import Company
from app.data_models.employee import Employee
from app.api.cert_tracker_api import CertTrackerAPI
from app.data_accessor.course_handler import CourseHandler
from app.data_accessor.company_handler import CompanyHandler
from app.data_accessor.employee_handler import EmployeeHandler
from app.data_models.employee_certificate import EmployeeCertificate
from app.data_accessor.employee_certificate_handler import EmployeeCertificateHandler
from app.data_processor.cert_tracker_service import CertTrackerService

class CertTrackerApp:
    """
    Sets up FastAPI app, services, and routes for the certificate tracker.
    """
    def __init__(self, data_dir: Path = Path("data")):
        self.data_dir = data_dir
        self.app = FastAPI(title="Certificate Manager")
        self._init_services()
        self._init_routes()

    def _init_services(self):
        course_handler = CourseHandler(self.data_dir / "courses.csv", Course)
        company_handler = CompanyHandler(self.data_dir / "company.csv", Company)
        employee_handler = EmployeeHandler(self.data_dir / "employees.csv", Employee)
        employee_cert_handler = EmployeeCertificateHandler(self.data_dir / "employee_certs.csv", EmployeeCertificate)

        self.cert_service = CertTrackerService(
            course_handler,
            company_handler,
            employee_handler,
            employee_cert_handler
        )

    def _init_routes(self):
        cert_tracker_api = CertTrackerAPI(self.cert_service)
        self.app.include_router(cert_tracker_api.router)

