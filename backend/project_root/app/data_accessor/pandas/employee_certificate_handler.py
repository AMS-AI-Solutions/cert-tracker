from pathlib import Path
from datetime import date, timedelta
from typing import Dict, List, Optional, Any, Hashable

import pandas as pd

from app.data_models.employee_certificate import EmployeeCertificate
from app.data_accessor.pandas.pandas_handler import PandasHandler
from app.data_accessor.interfaces.employee_certificate_handler_interface import (
    EmployeeCertificateHandlerInterface,
)

CertList = List[EmployeeCertificate]
IntMap = Dict[int, int]
StrMap = Dict[str, int]


class EmployeeCertificateHandler(
    PandasHandler[EmployeeCertificate],
    EmployeeCertificateHandlerInterface,
):
    """
    Query and cache EmployeeCertificate records in a Pandas DataFrame.
    """

    def __init__(self, file_path: Path):
        super().__init__(
            file_path=file_path,
            model=EmployeeCertificate,
            parse_dates=["issue_date", "expiry_date"],
            index_col=None,
        )
        # Convert pandas Timestamp → date for comparisons
        for col in ("issue_date", "expiry_date"):
            self.df[col] = self.df[col].dt.date

    def get_by_id(self, certificate_id: str) -> Optional[EmployeeCertificate]:
        return self.get_certificate_by_id(certificate_id)

    def get_certificate_by_id(self, certificate_id: str) -> Optional[EmployeeCertificate]:
        mask = self.df["certificate_id"].astype(str) == str(certificate_id)
        if not mask.any():
            return None
        row = self.df.loc[mask].iloc[0]
        data = row.to_dict()
        data["certificate_id"] = certificate_id
        return EmployeeCertificate(**data)

    def find_by_certificate_name(self, search_term: str) -> List[EmployeeCertificate]:
        mask = self.df["certificate_name"].str.contains(search_term, case=False, na=False)
        records: List[Dict[Hashable, Any]] = self.df.loc[mask].to_dict(orient="records")
        return [EmployeeCertificate.model_validate(r) for r in records]

    def count_certificates_by_employee(self) -> IntMap:
        # Series: index=employee_id, values=count
        return self.df["employee_id"].value_counts().to_dict()

    def count_certificates_by_course(self) -> StrMap:
        return self.df["course_id"].value_counts().to_dict()

    def group_certificates_by_employee(self) -> Dict[int, CertList]:
        groups: Dict[int, CertList] = {}
        for emp_id, grp in self.df.groupby("employee_id"):
            records = grp.to_dict(orient="records")
            groups[emp_id] = [EmployeeCertificate.model_validate(r) for r in records]
        return groups

    def group_certificates_by_course(self) -> Dict[str, CertList]:
        groups: Dict[str, CertList] = {}
        for course_id, grp in self.df.groupby("course_id"):
            records = grp.to_dict(orient="records")
            groups[course_id] = [EmployeeCertificate.model_validate(r) for r in records]
        return groups

    def get_employee_certificates_by_employee_id(self, employee_id: int) -> CertList:
        grp = self.df[self.df["employee_id"] == employee_id]
        return [EmployeeCertificate.model_validate(r) for r in grp.to_dict(orient="records")]

    def get_employee_certificates_by_course_id(self, course_id: str) -> CertList:
        grp = self.df[self.df["course_id"] == course_id]
        return [EmployeeCertificate.model_validate(r) for r in grp.to_dict(orient="records")]

    def get_certificates_expiring_in_time_range(
        self, start_date: date, end_date: date
    ) -> CertList:
        mask = (self.df["expiry_date"] >= start_date) & (self.df["expiry_date"] <= end_date)
        return [EmployeeCertificate.model_validate(r) for r in self.df.loc[mask].to_dict(orient="records")]

    def get_certificates_expiring_within(
        self, days: int, from_date: date
    ) -> CertList:
        cutoff = from_date + timedelta(days=days)
        return self.get_certificates_expiring_in_time_range(from_date, cutoff)

    def get_upcoming_expirations(self, days_ahead: int) -> CertList:
        today = date.today()
        return self.get_certificates_expiring_in_time_range(
            today, today + timedelta(days=days_ahead)
        )

    def count_expirations_by_company(self, days_ahead: int) -> Dict[str, int]:
        upcoming_df = pd.DataFrame(
            [c.__dict__ for c in self.get_upcoming_expirations(days_ahead)]
        )
        if upcoming_df.empty:
            return {}
        return upcoming_df["sponsoring_company"].value_counts().to_dict()  # type: ignore

    def certificates_by_employee_summary(self) -> Dict[int, List[str]]:
        # group certificate_name lists by employee_id
        return (
            self.df
            .groupby("employee_id")["certificate_name"]
            .apply(list)
            .to_dict()
        )
