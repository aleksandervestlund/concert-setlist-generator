import json
from pathlib import Path


def export_to_file(setlist: list[list[str]], filename: Path) -> None:
    with filename.open("w", encoding="utf-8") as file:
        json.dump(setlist, file, ensure_ascii=False, indent=2)


def import_from_file(filename: Path) -> list[list[str]]:
    with filename.open(encoding="utf-8") as file:
        return json.load(file)
