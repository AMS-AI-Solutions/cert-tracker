from pathlib import Path
from typing import Optional, Dict, Any
from app.data_models.employee import Employee
from app.data_accessor.pandas.pandas_handler import PandasHandler
from app.data_accessor.interfaces.employee_handler_interface import EmployeeHandlerInterface

class EmployeeHandler(PandasHandler[Employee], EmployeeHandlerInterface):
    def __init__(self, file_path: Path):
        super().__init__(
            file_path,
            Employee,
            index_col="employee_id"
        )

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        try:
            row_series = self.df.loc[employee_id]
        except KeyError:
            return None
        row: Dict[Any, Any] = row_series.to_dict()
        # Ensure keys are strings
        row_dict: Dict[str, Any] = {str(k): v for k, v in row.items()}
        row_dict["employee_id"] = employee_id
        return Employee(**row_dict)

    def get_company_name_from_employee_name(self, employee_name: str) -> Optional[str]:
        # Build lowercase full names Series
        full_names = self.df.apply(
            lambda r: f"{r['first_name']} {r['last_name']}", axis=1
        ).str.lower()
        target = employee_name.lower()
        matches = full_names[full_names == target]
        if matches.empty:
            return None
        emp_id = matches.index[0]
        return self.df.at[emp_id, 'company_name']
