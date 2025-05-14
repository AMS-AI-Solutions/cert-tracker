from pathlib import Path
typing: List, Type, Generic, TypeVar
import csv
T = TypeVar('T', bound=BaseModel)

class CsvHandler(Generic[T]):
    def __init__(self, file_path: Path, model: Type[T]):
        self.file_path = file_path
        self.model = model

    def load_all(self) -> List[T]:
        with self.file_path.open(newline='') as f:
            reader = csv.DictReader(f)
            return [self.model(**row) for row in reader]