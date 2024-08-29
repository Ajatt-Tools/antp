from gomi.common import find_referenced_media_files

EXAMPLE = """
@charset "UTF-8";
@import url("_ajt_japanese_24.7.14.1.css");
@font-face {
    font-family: "KanjiStrokeOrders";
    src: url("_kso.woff2");
}
@font-face {
    font-family: "Local Mincho";
    src: url("_yumin.woff2");
}
"""


def test_find_referenced_media() -> None:
    result = find_referenced_media_files(EXAMPLE)
    assert result == {"_ajt_japanese_24.7.14.1.css", "_kso.woff2", "_yumin.woff2"}
