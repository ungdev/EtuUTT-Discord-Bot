from __future__ import annotations

from functools import lru_cache
from os import getenv
from pathlib import PurePath

from etuutt_bot.types import ChannelId


def parse_roles(file: PurePath | str) -> dict[str, list[str]]:
    with open(file) as f:
        content = f.read().replace("\n", "").replace(" ", "").removesuffix(";")
    # after loading the file and removing spaces and linebreaks,
    # content should look like "CS:MATH01,PHYS11,PC12;TM:NF05,TNEV"

    ues = {}
    category_names = set(parse_categories().keys())
    for category in content.split(";"):
        cat_name, cat_ues = category.split(":")
        if cat_name in category_names:
            ues[cat_name] = [ue.strip() for ue in cat_ues.split(",")]

    return ues


@lru_cache(maxsize=None)
def parse_categories() -> dict[str, ChannelId]:
    categories = getenv("UES_CATEGORIES")
    if categories is None:
        raise KeyError("Environment variable missing : UES_CATEGORIES")
    result = {}
    for cat in categories.split(","):
        args = cat.split(":")
        if len(args) != 2:
            msg = f'UEs should be key/value pairs separated by a `:`. "{cat}" found instead'
            raise ValueError(msg)
        if not args[1].isdigit():
            raise ValueError("Category IDs should be valid integers")
        result[args[0]] = ChannelId(int(args[1]))
    return result
