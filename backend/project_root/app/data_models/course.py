from pydantic import BaseModel

class Course(BaseModel):
    course_id: int
    course_name: str
    certificate_name: str
    