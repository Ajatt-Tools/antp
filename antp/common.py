# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import dataclasses
import os
import re
from dataclasses import dataclass
from .consts import FONTS_DIR, NOTE_TYPES_DIR


class ANTPError(Exception):
    pass


@dataclass(frozen=True)
class CardTemplate:
    name: str
    front: str
    back: str


@dataclass(frozen=True)
class NoteType:
    name: str
    fields: list[str]
    css: str
    templates: list[CardTemplate]

    def rename(self, new_name: str):
        return dataclasses.replace(self, name=new_name)


def read_num(msg: str = "Input number: ", min_val: int = 0, max_val: int | None = None) -> int:
    try:
        resp = int(input(msg))
    except ValueError as ex:
        raise ANTPError(ex) from ex
    if resp < min_val or (max_val and resp > max_val):
        raise ANTPError("Value out of range.")
    return resp


def select(items: list[str], msg: str = "Select item number: ") -> str | None:
    if not items:
        print("Nothing to show.")
        return None

    for idx, model in enumerate(items):
        print(f"{idx}: {model}")
    print()

    idx = read_num(msg, max_val=len(items) - 1)
    return items[idx]


def get_used_fonts(template_css: str):
    return re.findall(r"url\([\"'](\w+\.(?:[ot]tf|woff\d?))[\"']\)", template_css, re.IGNORECASE)


def init():
    for path in (NOTE_TYPES_DIR, FONTS_DIR):
        path.mkdir(exist_ok=True)
