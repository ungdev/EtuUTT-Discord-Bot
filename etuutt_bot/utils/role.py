from __future__ import annotations

from pathlib import PurePath


def parse_roles(file: PurePath | str) -> dict[str, list[str]]:
    with open(file) as f:
        content = f.read().replace("\n", "").replace(" ", "").removesuffix(";")
    # after loading the file and removing spaces and linebreaks,
    # content should look like "CS:MATH01,PHYS11,PC12;TM:NF05,TNEV"

    ues = {}
    for category in content.split(";"):
        cat_name, cat_ues = category.split(":")
        ues[cat_name] = [ue.strip() for ue in cat_ues.split(",")]

    return ues
