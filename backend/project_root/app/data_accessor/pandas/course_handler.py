from pathlib import Path
#from typing import Optional, Dict, Any
from typing import Optional
from app.data_models.course import Course
from app.data_accessor.pandas.pandas_handler import PandasHandler
from app.data_accessor.interfaces.course_handler_interface import CourseHandlerInterface

class CourseHandler(PandasHandler[Course], CourseHandlerInterface):
    """
    Concrete implementation of CourseHandlerInterface using PandasHandler.
    """
    def __init__(self, file_path: Path):
        super().__init__(
            file_path,
            Course,
            index_col="course_id"
        )

    def get_by_id(self, course_id: str) -> Optional[Course]:
        """
         Retrieve a Course object based on its unique course ID
        """
        try:
            row_series = self.df.loc[course_id]
        except KeyError:
            return None
        row_dict = {str(k): v for k, v in row_series.to_dict().items()}
        row_dict["course_id"] = course_id
        return Course(**row_dict)
    
    def get_by_course_name_from_certificate_name(self, certificate_name: str) -> Optional[str]:
        """
        Retrieve the course name that corresponds to the given certificate name.
        """
        subset = self.df[self.df["certificate_name"] == certificate_name]
        if subset.empty:
            return None
        return subset.iloc[0]["course_name"]
