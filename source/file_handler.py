import json
from pathlib import Path


def export_to_file(setlist: list[list[str]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(setlist, file, ensure_ascii=False, indent=2)


def import_from_file(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8") as file:
        return json.load(file)
