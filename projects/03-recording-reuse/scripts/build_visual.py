"""Build the deterministic five-page recording-reuse carousel."""

from decimal import Decimal
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

if __package__:
    from scripts.data_contract import (
        load_catalog_summary,
        load_outlier,
        validate_evidence,
    )
else:
    from data_contract import load_catalog_summary, load_outlier, validate_evidence


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PNG_PATH = PROJECT_ROOT / "charts" / "recording-reuse.png"
CAROUSEL_DIR = PROJECT_ROOT / "carousel"

WIDTH = 1200
HEIGHT = 1500
COLUMNS = 15
ROWS = 12
PAGE_FILENAMES = (
    "page-01-hook.png",
    "page-02-reveal.png",
    "page-03-structure.png",
    "page-04-sql.png",
    "page-05-lesson.png",
)

COBALT = "#2446F5"
INK = "#0B0D12"
PAPER = "#F7F7F2"
ACID = "#D8FF3E"
PALE_BLUE = "#B9C9FF"

SUPPORT_TEXT_SIZES = {
    "sql_method": 34,
    "snapshot": 30,
    "catalog_limit": 30,
}


def medium_positions(
    columns: int = COLUMNS,
    rows: int = ROWS,
) -> list[tuple[int, int]]:
    """Return logical column/row positions for all 180 media."""
    return [(column, row) for row in range(rows) for column in range(columns)]


def track_marker_positions(
    columns: int = 6,
    rows: int = 4,
) -> list[tuple[int, int]]:
    """Return 24 logical marker positions for one medium."""
    return [(column, row) for row in range(rows) for column in range(columns)]


def carousel_page_paths(output_dir: Path) -> list[Path]:
    """Return the stable five-page carousel output paths."""
    return [output_dir / filename for filename in PAGE_FILENAMES]


def supporting_text_sizes() -> dict[str, int]:
    """Return required sizes that survive a 30% feed preview."""
    return dict(SUPPORT_TEXT_SIZES)


def _font(
    size: int,
    *,
    bold: bool = False,
    mono: bool = False,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a system font, with Pillow's bundled font as a fallback."""
    if mono:
        filenames = (
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/SFNSMono.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        )
    elif bold:
        filenames = (
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/SFNS.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        )
    else:
        filenames = (
            "/System/Library/Fonts/SFNS.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        )
    for filename in filenames:
        try:
            return ImageFont.truetype(filename, size=size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _new_page(page_number: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), COBALT)
    draw = ImageDraw.Draw(image)
    draw.text(
        (72, 48),
        "MUSICBRAINZ SQL STORIES / 03",
        font=_font(23, bold=True),
        fill=INK,
    )
    draw.text(
        (1128, 48),
        f"{page_number:02d} / 05",
        font=_font(23, bold=True),
        fill=INK,
        anchor="ra",
    )
    draw.line((72, 88, 1128, 88), fill=INK, width=3)
    return image, draw


def _save_page(image: Image.Image, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True)
    return path


def _draw_medium(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    *,
    width: int = 54,
    height: int = 28,
) -> None:
    """Draw one medium with exactly 24 visible matching-track markers."""
    draw.rectangle((x, y, x + width, y + height), outline=PALE_BLUE, width=1)
    for column, row in track_marker_positions():
        marker_x = x + 6 + column * 8
        marker_y = y + 5 + row * 5
        draw.rectangle(
            (marker_x, marker_y, marker_x + 2, marker_y + 2),
            fill=ACID,
        )


def _render_hook(
    outlier: dict[str, str | int],
    catalog: dict[str, Decimal],
) -> Image.Image:
    image, draw = _new_page(1)
    track_rows = int(outlier["track_appearances"])
    draw.text(
        (68, 138),
        f"{track_rows:,}",
        font=_font(210, bold=True),
        fill=INK,
    )
    draw.text(
        (78, 356),
        "TRACK ROWS FOR ONE RECORDING",
        font=_font(34, bold=True),
        fill=PAPER,
    )
    draw.rectangle((72, 500, 1128, 1270), fill=INK)
    draw.multiline_text(
        (106, 570),
        "I THOUGHT THIS\nRECORDING\nAPPEARED\nEVERYWHERE.",
        font=_font(78, bold=True),
        fill=PAPER,
        spacing=16,
    )
    draw.text(
        (106, 1168),
        "The query looked enormous.",
        font=_font(31),
        fill=PALE_BLUE,
    )
    draw.text(
        (72, 1366),
        "MusicBrainz full export / 2026-07-15",
        font=_font(SUPPORT_TEXT_SIZES["snapshot"], bold=True),
        fill=INK,
    )
    return image


def _render_reveal(
    outlier: dict[str, str | int],
    catalog: dict[str, Decimal],
) -> Image.Image:
    image, draw = _new_page(2)
    track_rows = int(outlier["track_appearances"])
    releases = int(outlier["distinct_releases"])
    draw.text((68, 138), f"{track_rows:,}", font=_font(180, bold=True), fill=INK)
    draw.text((78, 328), "TRACK ROWS", font=_font(38, bold=True), fill=PAPER)
    draw.text((76, 438), "BUT ONLY", font=_font(30, bold=True), fill=INK)
    draw.rectangle((72, 500, 1128, 1000), fill=INK)
    draw.text((104, 540), f"{releases}", font=_font(260, bold=True), fill=ACID)
    draw.text((418, 720), "RELEASE", font=_font(76, bold=True), fill=PAPER)
    draw.multiline_text(
        (106, 874),
        "My SQL was counting correctly.\nMy first interpretation was not.",
        font=_font(34, bold=True),
        fill=PALE_BLUE,
        spacing=15,
    )
    draw.text(
        (72, 1090),
        "RECORDING",
        font=_font(22, bold=True),
        fill=INK,
    )
    draw.multiline_text(
        (72, 1128),
        str(outlier["recording_name"]),
        font=_font(42, bold=True),
        fill=PAPER,
        spacing=8,
    )
    draw.text(
        (72, 1370),
        f"Release ID {outlier['release_id']}",
        font=_font(28, bold=True),
        fill=INK,
    )
    return image


def _render_structure(
    outlier: dict[str, str | int],
    catalog: dict[str, Decimal],
) -> Image.Image:
    image, draw = _new_page(3)
    media = int(outlier["distinct_mediums"])
    tracks_per_medium = int(outlier["min_matching_track_rows_per_medium"])
    track_rows = int(outlier["track_appearances"])
    positions = medium_positions()
    markers = track_marker_positions()
    if len(positions) != media or len(positions) * len(markers) != track_rows:
        raise ValueError("carousel marker geometry does not match checked evidence")

    draw.text(
        (72, 126),
        "ONE RELEASE CONTAINS THE WHOLE RESULT.",
        font=_font(43, bold=True),
        fill=INK,
    )
    draw.rectangle((72, 224, 1128, 934), fill=INK)
    draw.text(
        (96, 254),
        f"ONE RELEASE / ID {outlier['release_id']}",
        font=_font(22, bold=True),
        fill=ACID,
    )
    draw.text(
        (1104, 254),
        f"{media} MEDIA",
        font=_font(22, bold=True),
        fill=PALE_BLUE,
        anchor="ra",
    )
    grid_left = 96
    grid_top = 318
    column_step = 68
    row_step = 43
    for column, row in positions:
        _draw_medium(
            draw,
            grid_left + column * column_step,
            grid_top + row * row_step,
        )
    draw.text(
        (96, 858),
        f"{tracks_per_medium} MATCHING TRACK ROWS INSIDE EVERY MEDIUM",
        font=_font(22, bold=True),
        fill=PAPER,
    )
    draw.multiline_text(
        (72, 1000),
        f"{media} MEDIA × {tracks_per_medium} MATCHING\nTRACK ROWS = {track_rows:,}",
        font=_font(54, bold=True),
        fill=INK,
        spacing=8,
    )
    draw.text(
        (74, 1180),
        "release  ->  medium  ->  track",
        font=_font(31, bold=True, mono=True),
        fill=ACID,
        stroke_width=1,
        stroke_fill=INK,
    )
    draw.text(
        (72, 1370),
        "Each yellow marker is drawn from the checked 180 × 24 structure.",
        font=_font(28),
        fill=INK,
    )
    return image


def _render_sql(
    outlier: dict[str, str | int],
    catalog: dict[str, Decimal],
) -> Image.Image:
    image, draw = _new_page(4)
    draw.text(
        (72, 128),
        "FIRST, CHANGE THE RESULT GRAIN.",
        font=_font(50, bold=True),
        fill=INK,
    )
    draw.rectangle((72, 236, 1128, 820), fill=INK)
    code_lines = (
        "WITH recording_usage AS (",
        "    SELECT track.recording AS recording_id,",
        "           COUNT(track.id) AS track_appearances",
        "    FROM track",
        "    GROUP BY track.recording",
        ")",
    )
    code_y = 290
    for line in code_lines:
        draw.text(
            (104, code_y),
            line,
            font=_font(32, mono=True),
            fill=PAPER if "COUNT" not in line else ACID,
        )
        code_y += 76
    draw.text(
        (72, 888),
        "ONE RESULT ROW = ONE RECORDING",
        font=_font(37, bold=True),
        fill=INK,
    )
    draw.multiline_text(
        (72, 960),
        "COUNT(track.id) answers:\nHow many track rows?",
        font=_font(32, bold=True),
        fill=PAPER,
        spacing=10,
    )
    draw.multiline_text(
        (650, 960),
        "It does not answer:\nAcross how many releases?",
        font=_font(32, bold=True),
        fill=PAPER,
        spacing=10,
    )
    draw.rectangle((72, 1150, 1128, 1278), fill=ACID)
    draw.text(
        (100, 1182),
        "track  ->  medium  ->  release",
        font=_font(31, bold=True, mono=True),
        fill=INK,
    )
    draw.text(
        (100, 1230),
        "COUNT(DISTINCT release.id)",
        font=_font(31, bold=True, mono=True),
        fill=INK,
    )
    draw.text(
        (72, 1372),
        "The second count checks the interpretation, not the SQL syntax.",
        font=_font(28),
        fill=INK,
    )
    return image


def _render_lesson(
    outlier: dict[str, str | int],
    catalog: dict[str, Decimal],
) -> Image.Image:
    image, draw = _new_page(5)
    draw.multiline_text(
        (72, 144),
        "A CORRECT\nCOUNT CAN\nSTILL SUPPORT\nA WRONG\nINTERPRETATION.",
        font=_font(70, bold=True),
        fill=INK,
        spacing=12,
    )
    draw.rectangle((72, 720, 1128, 1040), fill=ACID)
    draw.multiline_text(
        (104, 770),
        "Before interpreting an aggregate,\nstate what one row represents\nand what the count actually measures.",
        font=_font(36, bold=True),
        fill=INK,
        spacing=14,
    )
    draw.rectangle((0, 1124, WIDTH, HEIGHT), fill=INK)
    draw.text(
        (72, 1162),
        "MusicBrainz full export / 2026-07-15",
        font=_font(SUPPORT_TEXT_SIZES["snapshot"], bold=True),
        fill=PALE_BLUE,
    )
    draw.multiline_text(
        (72, 1220),
        "Catalog metadata, not plays, sales,\naudience, or popularity.",
        font=_font(SUPPORT_TEXT_SIZES["catalog_limit"]),
        fill=PAPER,
        spacing=8,
    )
    draw.text(
        (72, 1370),
        "github.com/leodid68/musicbrainz-sql-stories",
        font=_font(28, bold=True),
        fill=ACID,
    )
    return image


def build_carousel_pages(output_dir: Path = CAROUSEL_DIR) -> list[Path]:
    """Render all five deterministic carousel pages."""
    validate_evidence()
    outlier = load_outlier()
    catalog = load_catalog_summary()
    renderers = (
        _render_hook,
        _render_reveal,
        _render_structure,
        _render_sql,
        _render_lesson,
    )
    paths = carousel_page_paths(output_dir)
    return [
        _save_page(renderer(outlier, catalog), path)
        for renderer, path in zip(renderers, paths, strict=True)
    ]


def build_visual(output_path: Path = PNG_PATH) -> Path:
    """Render page one as the standalone cover/export."""
    validate_evidence()
    return _save_page(
        _render_hook(load_outlier(), load_catalog_summary()),
        output_path,
    )


if __name__ == "__main__":
    build_carousel_pages()
    build_visual()
