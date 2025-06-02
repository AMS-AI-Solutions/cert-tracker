from pydantic import BaseModel

class Course(BaseModel):
    course_id: str
    course_name: str
    certificate_name: str
    