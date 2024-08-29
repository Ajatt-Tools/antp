# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import dataclasses
import re
from dataclasses import dataclass
from .consts import REPO_MEDIA_DIR, NOTE_TYPES_DIR


RE_MEDIA_IMPORT = re.compile(r"url\([\"']([\w_.]+\.(?:[ot]tf|woff\d?|css))[\"']\)", flags=re.IGNORECASE)


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


def find_referenced_media_files(template_css: str) -> frozenset[str]:
    return frozenset(re.findall(RE_MEDIA_IMPORT, template_css))


def init():
    for path in (NOTE_TYPES_DIR, REPO_MEDIA_DIR):
        path.mkdir(exist_ok=True)
