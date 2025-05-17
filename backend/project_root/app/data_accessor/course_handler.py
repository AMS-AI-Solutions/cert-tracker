from pathlib import Path
from typing import List, Optional


from app.data_models.course import Course
from app.data_accessor.csv_handler import CsvHandler

class CourseHandler(CsvHandler[Course]):
    """
    handles course data loaded from a csv file
    """

    def __init__(self, file_path: Path):
        super().__init__(file_path, Course)
        self._cache: Optional[List[Course]] = None

    def load_all(self) -> List[Course]:
        """Load and cache all employees from CSV."""

        if self._cache is None:
            self._cache = super().load_all()
        return self._cache
    
    def get_by_name(self, certificate_name: str) -> Optional[Course]:
        """Retrives a course name by the certificate name"""

        return next((course.course_name for course in self.load_all() if course.certificate_name == certificate_name), None)
    

    def get_name_by_id(self, course_id: str) -> Optional[Course]:
        """Retrives a course name by course id"""

        return next((course.course_name for course in self.load_all() if course.course_id == course_id), None)

        




    

