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
        # Load CSV into DataFrame with optional date parsing
        self.df = pd.read_csv(file_path, parse_dates=parse_dates or [])
        # Set index for lookups if provided
        if index_col:
            self.df.set_index(index_col, inplace=True)

    def load_all(self) -> List[T]:
        # Convert DataFrame rows to list of Pydantic models
        records = self.df.reset_index().to_dict(orient="records")  # List[Dict[str, Any]]
        result: List[T] = []
        for rec in records:
            # Ensure keys are strings for ** unpacking
            rec_dict: Dict[str, Any] = {str(k): v for k, v in rec.items()}
            result.append(self.model(**rec_dict))
        return result
