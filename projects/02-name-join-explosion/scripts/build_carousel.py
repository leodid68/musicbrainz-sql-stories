from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

from scripts.build_chart import PNG_PATH, build_chart, load_metrics


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "output"
    / "pdf"
    / "musicbrainz-sql-stories-02.pdf"
)

WIDTH, HEIGHT = 1080, 1350
BACKGROUND = HexColor("#F7F3EA")
INK = HexColor("#172A3A")
MUTED = HexColor("#48606F")
ACCENT = HexColor("#E0784F")
SECONDARY = HexColor("#78A99F")
WHITE = HexColor("#FFFFFF")
GRID = HexColor("#DDD6C9")


def draw_page_base(canvas: Canvas, page_number: int) -> None:
    canvas.setFillColor(BACKGROUND)
    canvas.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 20)
    canvas.drawString(72, 1285, "MusicBrainz SQL Stories #2")
    canvas.drawRightString(WIDTH - 72, 58, f"{page_number}/5")


def draw_lines(
    canvas: Canvas,
    lines: list[str],
    x: float,
    y: float,
    font: str,
    size: float,
    leading: float,
    color=INK,
) -> float:
    canvas.setFillColor(color)
    canvas.setFont(font, size)
    for line in lines:
        canvas.drawString(x, y, line)
        y -= leading
    return y


def wrap_text(
    text: str,
    font: str,
    size: float,
    max_width: float,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if not current or stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_metric_card(
    canvas: Canvas,
    x: float,
    y: float,
    width: float,
    value: str,
    label: str,
    color,
) -> None:
    canvas.setFillColor(WHITE)
    canvas.roundRect(x, y, width, 210, 24, fill=1, stroke=0)
    canvas.setFillColor(color)
    canvas.roundRect(x, y + 194, width, 16, 8, fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.setFont("Helvetica-Bold", 60)
    canvas.drawCentredString(x + width / 2, y + 105, value)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica-Bold", 23)
    canvas.drawCentredString(x + width / 2, y + 55, label)


def draw_cover(canvas: Canvas, metrics: dict[str, int | float]) -> None:
    draw_page_base(canvas, 1)
    canvas.setFillColor(ACCENT)
    canvas.roundRect(72, 1090, 245, 44, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawCentredString(194, 1104, "SQL + JOIN CARDINALITY")

    draw_lines(
        canvas,
        ["Valid SQL.", "Wrong dataset."],
        72,
        930,
        "Helvetica-Bold",
        78,
        90,
    )
    draw_lines(
        canvas,
        [
            "What happened when I joined",
            "MusicBrainz artists on name?",
        ],
        72,
        690,
        "Helvetica",
        35,
        50,
        MUTED,
    )

    draw_metric_card(
        canvas,
        72,
        315,
        430,
        "2.93M",
        "rows before JOIN",
        SECONDARY,
    )
    draw_metric_card(
        canvas,
        578,
        315,
        430,
        "5.38M",
        "rows after JOIN",
        ACCENT,
    )
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 31)
    canvas.drawCentredString(
        WIDTH / 2,
        245,
        f"+{float(metrics['row_increase_pct']):.2f}% without a syntax error",
    )


def draw_multiplication(
    canvas: Canvas,
    metrics: dict[str, int | float],
) -> None:
    draw_page_base(canvas, 2)
    draw_lines(
        canvas,
        ["Why 249 entities", "became 62,001 rows."],
        72,
        1120,
        "Helvetica-Bold",
        58,
        70,
    )

    canvas.setFillColor(WHITE)
    canvas.roundRect(72, 700, WIDTH - 144, 245, 24, fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.setFont("Helvetica-Bold", 58)
    canvas.drawCentredString(WIDTH / 2, 840, "249 x 249 = 62,001")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 26)
    canvas.drawCentredString(
        WIDTH / 2,
        775,
        "Every Indigo row matched every other Indigo row.",
    )

    canvas.setFillColor(SECONDARY)
    canvas.roundRect(72, 420, WIDTH - 144, 185, 24, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 42)
    canvas.drawCentredString(310, 535, "249")
    canvas.setFont("Helvetica-Bold", 38)
    canvas.drawCentredString(310, 481, "same-ID matches")
    canvas.setFillColor(ACCENT)
    canvas.roundRect(548, 420, 460, 185, 24, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 42)
    canvas.drawCentredString(
        778,
        535,
        f"{int(metrics['indigo_cross_entity_matches']):,}",
    )
    canvas.setFont("Helvetica-Bold", 34)
    canvas.drawCentredString(778, 481, "cross-entity matches")
    draw_lines(
        canvas,
        wrap_text(
            "The query ran correctly. The join key created the wrong grain.",
            "Helvetica-Bold",
            30,
            WIDTH - 144,
        ),
        72,
        300,
        "Helvetica-Bold",
        30,
        40,
    )


def draw_chart_page(canvas: Canvas) -> None:
    draw_page_base(canvas, 3)
    draw_lines(
        canvas,
        ["The extra rows came from", "different artist IDs."],
        72,
        1150,
        "Helvetica-Bold",
        54,
        64,
    )
    canvas.setFillColor(WHITE)
    canvas.roundRect(48, 220, WIDTH - 96, 760, 24, fill=1, stroke=0)
    chart = ImageReader(str(PNG_PATH))
    canvas.drawImage(
        chart,
        70,
        290,
        width=940,
        height=588,
        preserveAspectRatio=True,
        mask="auto",
    )
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 25)
    canvas.drawString(72, 165, "2,448,276 cross-entity matches.")


def draw_join_checklist(canvas: Canvas) -> None:
    draw_page_base(canvas, 4)
    draw_lines(
        canvas,
        ["Three questions", "before every JOIN."],
        72,
        1120,
        "Helvetica-Bold",
        58,
        70,
    )

    cards = [
        (
            "1",
            "GRAIN",
            "What does one row represent in each input?",
            SECONDARY,
        ),
        (
            "2",
            "KEY",
            "Does the column identify an entity or only describe it?",
            ACCENT,
        ),
        (
            "3",
            "CARDINALITY",
            "How many rows should one input row match?",
            SECONDARY,
        ),
    ]
    y = 805
    for number, label, explanation, color in cards:
        canvas.setFillColor(WHITE)
        canvas.roundRect(72, y, WIDTH - 144, 190, 24, fill=1, stroke=0)
        canvas.setFillColor(color)
        canvas.circle(135, y + 95, 37, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 28)
        canvas.drawCentredString(135, y + 85, number)
        canvas.setFillColor(INK)
        canvas.setFont("Helvetica-Bold", 25)
        canvas.drawString(205, y + 120, label)
        draw_lines(
            canvas,
            wrap_text(explanation, "Helvetica", 25, 720),
            205,
            y + 75,
            "Helvetica",
            25,
            34,
            MUTED,
        )
        y -= 230

    canvas.setFillColor(INK)
    canvas.roundRect(72, 170, WIDTH - 144, 120, 22, fill=1, stroke=0)
    draw_lines(
        canvas,
        [
            "artist.name = descriptive attribute",
            "artist.id / artist.gid = catalog identifiers",
        ],
        112,
        240,
        "Courier",
        23,
        34,
        WHITE,
    )


def draw_limits_and_next(canvas: Canvas) -> None:
    draw_page_base(canvas, 5)
    draw_lines(
        canvas,
        ["What this analysis", "does not prove."],
        72,
        1120,
        "Helvetica-Bold",
        58,
        70,
    )

    limitations = [
        "This was a controlled self-join, not a production incident.",
        "Exact primary names only. Aliases were excluded.",
        "[unknown] and [no artist] were excluded.",
        "Different catalog IDs do not prove different real-world people.",
    ]
    y = 865
    for limitation in limitations:
        canvas.setFillColor(ACCENT)
        canvas.circle(92, y + 9, 8, fill=1, stroke=0)
        draw_lines(
            canvas,
            wrap_text(limitation, "Helvetica", 27, 820),
            125,
            y,
            "Helvetica",
            27,
            36,
        )
        y -= 115

    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(2)
    canvas.line(72, 410, WIDTH - 72, 410)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica-Bold", 22)
    canvas.drawString(72, 355, "NEXT EPISODE")
    draw_lines(
        canvas,
        ["Why is a track not always", "the same as a recording?"],
        72,
        285,
        "Helvetica-Bold",
        39,
        52,
    )
    canvas.setFillColor(SECONDARY)
    canvas.roundRect(72, 135, 385, 54, 27, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawCentredString(264, 153, "MusicBrainz SQL Stories #3")


def build_carousel(output: Path = DEFAULT_OUTPUT) -> Path:
    if not PNG_PATH.is_file():
        build_chart()

    output.parent.mkdir(parents=True, exist_ok=True)
    metrics = load_metrics()
    canvas = Canvas(str(output), pagesize=(WIDTH, HEIGHT))

    pages = [
        lambda page: draw_cover(page, metrics),
        lambda page: draw_multiplication(page, metrics),
        draw_chart_page,
        draw_join_checklist,
        draw_limits_and_next,
    ]
    for draw_page in pages:
        draw_page(canvas)
        canvas.showPage()

    canvas.save()
    return output


if __name__ == "__main__":
    build_carousel()
