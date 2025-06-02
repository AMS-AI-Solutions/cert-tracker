from pydantic import BaseModel
from datetime import date

class EmployeeCertificate(BaseModel):
    employee_id: int
    course_id: str
    certificate_name: str
    certificate_id: str
    issue_date: date
    expiry_date: date