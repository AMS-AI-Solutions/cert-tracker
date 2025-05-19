from pathlib import Path
from typing import Optional, Dict, Any
from app.data_models.company import Company
from app.data_accessor.pandas.pandas_handler import PandasHandler
from app.data_accessor.interfaces.company_handler_interface import CompanyHandlerInterface

class CompanyHandler(PandasHandler[Company], CompanyHandlerInterface):
    def __init__(self, file_path: Path):
        super().__init__(
            file_path,
            Company,
            index_col="company_id"
        )

    def get_by_id(self, company_id: int) -> Optional[Company]:
        try:
            row_series = self.df.loc[company_id]
        except KeyError:
            return None
        row: Dict[Any, Any] = row_series.to_dict()
        row_dict: Dict[str, Any] = {str(k): v for k, v in row.items()}
        row_dict["company_id"] = company_id
        return Company(**row_dict)

    def get_company_from_company_name(self, company_name: str) -> Optional[Company]:
        subset = self.df[self.df["company_name"] == company_name]
        if subset.empty:
            return None

        row_series = subset.iloc[0]
        row_dict: Dict[str, Any] = row_series.to_dict()
        row_dict["company_id"] = row_series.name
        return Company(**{str(k): v for k, v in row_dict.items()})
