from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Optional
from app.data_models.employee_certificate import EmployeeCertificate

class EmployeeCertificateHandlerInterface(ABC):
    @abstractmethod
    def load_all(self) -> List[EmployeeCertificate]: ...
    
    @abstractmethod
    def get_by_id(self, name: int) -> Optional[EmployeeCertificate]: ...

    @abstractmethod
    def get_certificates_expiring_in_time_range(self, start_data: datetime, end_data: datetime) -> Optional[List[EmployeeCertificate]]: ...