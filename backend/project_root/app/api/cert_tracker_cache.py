from pathlib import Path
from functools import lru_cache
from fastapi import FastAPI, Depends

from app.data_models.course import Course
from app.data_models.employee import Employee
from app.data_accessor.course_handler import CourseHandler
from app.data_accessor.employee_handler import EmployeeHandler
from app.data_models.employee_certificate import EmployeeCertificate
from app.data_processor.cert_tracker_service import CertTrackerService
from app.data_accessor.employee_certificate_handler import EmployeeCertificateHandler

from functools import lru_cache # Dependency factories (load CSVs once via lru_cache)

app = FastAPI(title="Certificate Manager")

@lru_cache()
def get_employee_repo():
    return EmployeeHandler(Path("data/employees.csv"), Employee)

@lru_cache()
def get_course_repo():
    return CourseHandler(Path("data/courses.csv"), Course)

@lru_cache()
def get_employee_cert_repo():
    return EmployeeCertificateHandler(Path("data/employee_certs.csv"), EmployeeCertificate)

@lru_cache()
def get_service(
    emp_cert_repo=Depends(get_employee_cert_repo),
    course_repo=Depends(get_course_repo),
    emp_repo=Depends(get_employee_repo),
):
    return CertTrackerService(emp_cert_repo, course_repo, emp_repo)
