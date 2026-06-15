import re
from itertools import chain
from typing import Any

from source.types import Setlists


def snake_to_camel(name: str) -> str:
    words = name.split("_")
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


def camel_to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def deep_snake_case_keys(data: Any) -> Any:
    if isinstance(data, dict):
        new_dict: dict[str, Any] = {}

        for k, v in data.items():
            new_key = "with_" if k == "with" else camel_to_snake(k)
            new_dict[new_key] = deep_snake_case_keys(v)

        return new_dict
    if isinstance(data, list):
        return [deep_snake_case_keys(item) for item in data]
    return data


def extract_setlists(setlists: Setlists) -> list[list[str]]:
    cleaned: list[list[str]] = []
    setlist = setlists.setlist

    for sl in setlist:
        sets = sl.sets

        if not (set_ := sets.set):
            continue

        songs = chain.from_iterable(set_.song for set_ in set_)

        if subcleaned := [
            song.name for song in songs if song.name.strip() != ""
        ]:
            cleaned.append(subcleaned)

    return cleaned
