from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from app.data_models.company import Company

class CourseHandlerInterface(ABC):
    @abstractmethod
    def load_all(self) -> List[Company]: ...
   
    @abstractmethod
    def get_by_id(self, company_id: str) -> Optional[Company]: ...

    @abstractmethod
    def get_by_company_from_company_name(self, certificate_name: str) -> Optional[Company]: ...