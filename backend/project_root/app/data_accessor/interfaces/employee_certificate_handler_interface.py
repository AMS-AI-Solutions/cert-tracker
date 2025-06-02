from datetime import date
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.data_models.employee_certificate import EmployeeCertificate

class EmployeeCertificateHandlerInterface(ABC):
    @abstractmethod
    def load_all(self) -> List[EmployeeCertificate]:
        """Load and return all certificates."""
        ...

    @abstractmethod
    def get_by_id(self, certificate_id: str) -> Optional[EmployeeCertificate]:
        """Retrieve a single certificate by its unique ID."""
        ...

    @abstractmethod
    def find_by_certificate_name(self, search_term: str) -> List[EmployeeCertificate]:
        """Return certificates whose name contains the search term (case-insensitive)."""
        ...

    @abstractmethod
    def count_certificates_by_employee(self) -> Dict[int, int]:
        """Map each employee_id to the number of certificates they hold."""
        ...

    @abstractmethod
    def count_certificates_by_course(self) -> Dict[str, int]:
        """Map each course_id to the number of certificates issued."""
        ...

    @abstractmethod
    def group_certificates_by_employee(self) -> Dict[int, List[EmployeeCertificate]]:
        """Group certificates into lists keyed by employee_id."""
        ...

    @abstractmethod
    def group_certificates_by_course(self) -> Dict[int, List[EmployeeCertificate]]:
        """Group certificates into lists keyed by course_id."""
        ...

    @abstractmethod
    def get_employee_certificates_by_employee_id(self, employee_id: int) -> List[EmployeeCertificate]:
        """Return all certificates for the given employee."""
        ...

    @abstractmethod
    def get_employee_certificates_by_course_id(self, course_id: str) -> List[EmployeeCertificate]:
        """Return all certificates for the given course."""
        ...

    @abstractmethod
    def get_certificates_expiring_in_time_range(
        self, start_date: date, end_date: date
    ) -> List[EmployeeCertificate]:
        """Return certificates whose expiry_date falls between start_date and end_date, inclusive."""
        ...

    @abstractmethod
    def get_certificates_expiring_within(
        self, days: int, from_date: date
    ) -> List[EmployeeCertificate]:
        """Return certificates expiring within `days` days of `from_date`."""
        ...

    @abstractmethod
    def get_upcoming_expirations(self, days_ahead: int) -> List[EmployeeCertificate]:
        """Return certificates expiring within the next `days_ahead` days."""
        ...

    @abstractmethod
    def count_expirations_by_company(self, days_ahead: int) -> Dict[str, int]:
        """Count how many certificates per sponsoring company expire within `days_ahead` days."""
        ...

    @abstractmethod
    def certificates_by_employee_summary(self) -> Dict[int, List[str]]:
        """Map each employee_id to the list of their certificate names."""
        ...
