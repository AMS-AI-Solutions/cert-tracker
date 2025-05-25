import pandas as pd
from pathlib import Path
from pydantic import BaseModel
from typing import Generic, Type, TypeVar, List, Optional, Dict, Any

T = TypeVar("T", bound=BaseModel)

class PandasHandler(Generic[T]):
    def __init__(
        self,
        file_path: Path,
        model: Type[T],
        parse_dates: Optional[List[str]] = None,
        index_col: Optional[str] = None,
    ):
        self.file_path = file_path
        self.model = model
        self.df = pd.read_csv(file_path, parse_dates=parse_dates or [])
        if index_col:
            self.df.set_index(index_col, inplace=True)

