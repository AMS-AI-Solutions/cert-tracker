from abc import ABC, abstractmethod
from typing import List, Optional
from app.data_models.course import Course

class CourseHandlerInterface(ABC):
    @abstractmethod
    def load_all(self) -> List[Course]: ...
   
    @abstractmethod
    def get_by_id(self, course_id: str) -> Optional[Course]: ...

    @abstractmethod
    def get_by_course_name_from_certificate_name(self, certificate_name: str) -> Optional[str]: ...