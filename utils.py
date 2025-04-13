from pathlib import Path
from typing import List


def validate_files(file_paths: List[str]) -> None:
    for path in file_paths:
        if not Path(path).exists():
            raise FileNotFoundError(f"Файл не найден: {path}")
