# Importer imports note types from ../templates/ to Anki.
# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU GPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import json
import os
from typing import Any, Collection, Iterable, Sequence

from .ankiconnect import invoke, request_model_names
from .common import CardTemplate, NoteType, find_referenced_media_files, select
from .consts import NOTE_TYPES_DIR, CSS_FILENAME, FRONT_FILENAME, BACK_FILENAME, JSON_FILENAME, REPO_MEDIA_DIR


def read_css(model_dir_name: str) -> str:
    with open(NOTE_TYPES_DIR / model_dir_name / CSS_FILENAME, encoding="utf8") as f:
        return f.read()


def read_card_templates(model_dir_name: str, template_names: list[str]) -> list[CardTemplate]:
    templates = []
    for template_name in template_names:
        dir_path = NOTE_TYPES_DIR / model_dir_name / template_name
        with (
            open(dir_path / FRONT_FILENAME, encoding="utf8") as front,
            open(dir_path / BACK_FILENAME, encoding="utf8") as back,
        ):
            templates.append(CardTemplate(template_name, front.read(), back.read()))
    return templates


def read_model_dict(model_dir_name: str) -> dict[str, Any]:
    with open(os.path.join(NOTE_TYPES_DIR, model_dir_name, JSON_FILENAME), encoding="utf8") as f:
        return json.load(f)


def read_model(model_dir_name: str) -> NoteType:
    model_dict = read_model_dict(model_dir_name)
    return NoteType(
        name=model_dict["modelName"],
        fields=model_dict["inOrderFields"],
        css=read_css(model_dir_name),
        templates=read_card_templates(model_dir_name, model_dict["cardTemplates"]),
    )


def format_import(model: NoteType) -> dict[str, Any]:
    return {
        "modelName": model.name,
        "inOrderFields": model.fields,
        "css": model.css,
        "cardTemplates": [
            {
                "Name": template.name,
                "Front": template.front,
                "Back": template.back,
            }
            for template in model.templates
        ],
    }


def send_note_type(model: NoteType):
    template_json = format_import(model)
    while template_json["modelName"] in request_model_names():
        template_json["modelName"] = input("Model with this name already exists. Enter new name: ")
    invoke("createModel", **template_json)


def save_files_to_anki_col(file_names: frozenset[str]) -> None:
    """
    Take a list of files and save them to Anki's 'collection.media' folder.
    The files should exist in the "media" folder on disk.
    """
    for file_name in file_names:
        full_path = os.path.join(REPO_MEDIA_DIR, file_name)
        if not os.path.isfile(full_path):
            print(f"not found on disk: '{full_path}'")
            continue
        invoke("storeMediaFile", filename=file_name, path=full_path)
        print(f"saved file in Anki collection: '{file_name}'")


def import_note_type() -> None:
    """
    Select a note type and add it to the currently opened Anki profile using AnkiConnect.
    """
    if model_dir_name := select(os.listdir(NOTE_TYPES_DIR)):
        print(f"Selected model: {model_dir_name}")
        model = read_model(model_dir_name)
        send_note_type(model)
        save_files_to_anki_col(find_referenced_media_files(model.css))
        print("Done.")
