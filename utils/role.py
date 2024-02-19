from __future__ import annotations

from functools import lru_cache
from os import getenv
from pathlib import PurePath


async def parse_roles(file: PurePath | str) -> dict[str, list[str]]:
    with open(file, "rt") as f:
        lines = f.readlines()

    raw_ues = ""
    for line in lines:
        raw_ues += line.strip()

    ues = {}
    for category in raw_ues.split(";"):
        if category != "" and category in parse_categories().keys():
            ues[category.split(":")[0]] = category.split(":")[1].split(",")

    return ues


@lru_cache(maxsize=None)
def parse_categories() -> dict[str, int]:
    if getenv("UES_CATEGORIES") is not None:
        categories = {}
        for category in getenv("UES_CATEGORIES").split(","):
            categories[category.split(":")[0].upper()] = int(category.split(":")[1])
        return categories
