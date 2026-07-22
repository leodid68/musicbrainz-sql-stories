"""Build the editorial recording-reuse visual from checked CSV evidence."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

if __package__:
    from scripts.data_contract import load_outlier, validate_evidence
else:
    from data_contract import load_outlier, validate_evidence


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PNG_PATH = PROJECT_ROOT / "charts" / "recording-reuse.png"

WIDTH = 1200
HEIGHT = 1500
COLUMNS = 15
ROWS = 12

DARK_NAVY = "#071521"
OFF_WHITE = "#F5F1E8"
CYAN = "#4DD6C8"
CORAL = "#FF7657"
MUTED_BLUE = "#7795A6"

SUPPORT_TEXT_SIZES = {
    "sql_method": 32,
    "snapshot": 28,
    "catalog_limit": 28,
}


def medium_positions(
    columns: int = COLUMNS,
    rows: int = ROWS,
) -> list[tuple[int, int]]:
    """Return logical column/row positions for every medium in the grid."""
    return [(column, row) for row in range(rows) for column in range(columns)]


def supporting_text_sizes() -> dict[str, int]:
    """Return sizes for required lines that must survive a 30% feed preview."""
    return dict(SUPPORT_TEXT_SIZES)


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a system sans font, with Pillow's bundled font as a fallback."""
    filenames = (
        (
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/SFNS.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        )
        if bold
        else (
            "/System/Library/Fonts/SFNS.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        )
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


def _draw_medium(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    *,
    width: int = 48,
    height: int = 18,
) -> None:
    """Draw one compact medium symbol."""
    draw.rounded_rectangle(
        (x, y, x + width, y + height),
        radius=height // 2,
        outline=CYAN,
        width=2,
    )
    draw.ellipse(
        (x + width - 12, y + 5, x + width - 6, y + 11),
        fill=CORAL,
    )


def build_visual(output_path: Path = PNG_PATH) -> Path:
    """Render and save the 1200-by-1500 recording-reuse editorial poster."""
    validate_evidence()
    outlier = load_outlier()

    track_rows = int(outlier["track_appearances"])
    releases = int(outlier["distinct_releases"])
    media = int(outlier["distinct_mediums"])
    tracks_per_medium = int(outlier["min_matching_track_rows_per_medium"])
    positions = medium_positions()
    if len(positions) != media:
        raise ValueError("visual grid does not match checked medium count")

    image = Image.new("RGB", (WIDTH, HEIGHT), DARK_NAVY)
    draw = ImageDraw.Draw(image)

    # Editorial masthead and mistaken first interpretation.
    draw.text(
        (72, 54),
        "MUSICBRAINZ SQL STORIES / 03",
        font=_font(23, bold=True),
        fill=CYAN,
    )
    draw.line((72, 92, 1128, 92), fill="#173547", width=2)
    draw.multiline_text(
        (72, 126),
        "I thought this recording\nappeared everywhere.",
        font=_font(70, bold=True),
        fill=OFF_WHITE,
        spacing=3,
    )

    # The hero contrast is intentionally dominant over the SQL method.
    draw.text((72, 322), f"{track_rows:,}", font=_font(118, bold=True), fill=OFF_WHITE)
    draw.text((79, 445), "TRACK ROWS", font=_font(30, bold=True), fill=MUTED_BLUE)
    draw.line((690, 337, 690, 486), fill="#244657", width=2)
    draw.text((756, 322), f"{releases:,}", font=_font(118, bold=True), fill=CORAL)
    draw.text((764, 445), "RELEASE", font=_font(30, bold=True), fill=MUTED_BLUE)

    recording_name = str(outlier["recording_name"])
    draw.text((72, 516), "RECORDING", font=_font(20, bold=True), fill=MUTED_BLUE)
    draw.text((72, 546), recording_name, font=_font(36, bold=True), fill=OFF_WHITE)

    # One outlined release literally contains the 180 medium symbols.
    container = (72, 620, 1128, 1089)
    draw.rounded_rectangle(container, radius=22, outline=MUTED_BLUE, width=3)
    draw.rounded_rectangle((98, 596, 424, 645), radius=16, fill=CORAL)
    draw.text(
        (116, 608),
        f"ONE RELEASE / ID {outlier['release_id']}",
        font=_font(21, bold=True),
        fill=DARK_NAVY,
    )

    grid_left = 118
    grid_top = 681
    column_step = 65
    row_step = 27
    for column, row in positions:
        _draw_medium(
            draw,
            grid_left + column * column_step,
            grid_top + row * row_step,
        )

    annotation_y = 1020
    draw.line((118, annotation_y, 164, annotation_y), fill=CYAN, width=3)
    draw.text(
        (182, annotation_y - 16),
        f"{tracks_per_medium} matching track rows per medium",
        font=_font(25, bold=True),
        fill=OFF_WHITE,
    )
    draw.text(
        (1080, annotation_y - 16),
        f"{media} MEDIA",
        font=_font(25, bold=True),
        fill=CYAN,
        anchor="ra",
    )

    # Explanation and hierarchy remain readable, while method stays secondary.
    equation = f"{media} media x {tracks_per_medium} tracks = {track_rows:,}"
    draw.text((72, 1138), equation, font=_font(49, bold=True), fill=OFF_WHITE)
    draw.text(
        (74, 1213),
        "release  ->  medium  ->  track",
        font=_font(27, bold=True),
        fill=CYAN,
    )

    draw.rounded_rectangle(
        (72, 1264, 1128, 1360),
        radius=18,
        fill="#0D2230",
        outline="#244657",
        width=2,
    )
    draw.text((101, 1296), "SQL TECHNIQUE", font=_font(20, bold=True), fill=MUTED_BLUE)
    draw.text(
        (292, 1287),
        "COUNT(track.id) vs COUNT(DISTINCT release.id)",
        font=_font(SUPPORT_TEXT_SIZES["sql_method"]),
        fill=OFF_WHITE,
    )

    draw.line((72, 1391, 1128, 1391), fill="#173547", width=2)
    draw.text(
        (72, 1407),
        "MusicBrainz full export / 2026-07-15",
        font=_font(SUPPORT_TEXT_SIZES["snapshot"], bold=True),
        fill=MUTED_BLUE,
    )
    draw.text(
        (72, 1446),
        "Catalog metadata, not plays, sales, or popularity.",
        font=_font(SUPPORT_TEXT_SIZES["catalog_limit"]),
        fill=MUTED_BLUE,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=True)
    return output_path


if __name__ == "__main__":
    build_visual()
