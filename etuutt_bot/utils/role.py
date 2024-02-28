from __future__ import annotations

from functools import lru_cache
from os import getenv
from pathlib import PurePath


async def parse_roles(file: PurePath | str) -> dict[str, list[str]]:
    with open(file) as f:
        lines = f.readlines()

    raw_ues = ""
    for line in lines:
        raw_ues += line.strip()

    ues = {}
    for category in raw_ues.split(";"):
        if category != "" and category.split(":")[0] in parse_categories():
            ues[category.split(":")[0]] = category.split(":")[1].split(",")

    return ues


@lru_cache(maxsize=None)
def parse_categories() -> dict[str, int]:
    categories = getenv("UES_CATEGORIES")
    if categories is None:
        raise KeyError("Environment variable missing : UES_CATEGORIES")
    result = {}
    for cat in categories.split(","):
        args = cat.split(":")
        if len(args) != 2:
            msg = "UES should be key/value pairs separated by a `:`." f' "{cat}" found instead'
            raise ValueError(msg)
        if not args[1].isdigit():
            raise ValueError("Categories ids should be valid ids")
        result[args[0]] = int(args[1])
    return result
