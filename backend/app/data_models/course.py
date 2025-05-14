from pydantic import BaseModel, EmailStr
from datetime import date

class Course(BaseModel):
    course_id: str
    course_name: str
    certificate_type: str
    default_issue_date: date
    default_expiry_date: date