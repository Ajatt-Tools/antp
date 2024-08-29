# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import pathlib

JSON_INDENT = 4
JSON_FILENAME = "template.json"
CSS_FILENAME = "template.css"
FRONT_FILENAME = "front.html"
BACK_FILENAME = "back.html"
README_FILENAME = "README.md"
THIS_DIR = pathlib.Path.cwd()
NOTE_TYPES_DIR = THIS_DIR / "templates"
REPO_MEDIA_DIR = THIS_DIR / "media"
