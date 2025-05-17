from pathlib import Path
from typing import Generic, Type, TypeVar, List, Optional
from pydantic import BaseModel
import pandas as pd

T = TypeVar("T", bound=BaseModel)

class PandasHandler(Generic[T]):
    """
    Generic base for any Pydantic-backed CSV repository.
    It loads a CSV file into a DataFrame and converts rows to Pydantic models.
    """
    def __init__(
        self,
        file_path: Path,
        model: Type[T],
        parse_dates: Optional[List[str]] = None,
        index_col: Optional[str] = None,
    ):
        self.file_path = file_path
        self.model = model
        # Load CSV into DataFrame with optional date parsing
        self.df = pd.read_csv(file_path, parse_dates=parse_dates or [])
        # If specified, set an index for lookups
        if index_col:
            self.df.set_index(index_col, inplace=True)

    def load_all(self) -> List[T]:
        records = self.df.reset_index().to_dict(orient="records")
        return [self.model(**row) for row in records]