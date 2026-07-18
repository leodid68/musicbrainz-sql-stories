from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHART_PATH = PROJECT_ROOT / "charts" / "top-duplicated-names.png"
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "output"
    / "pdf"
    / "musicbrainz-sql-stories-01.pdf"
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
    canvas.drawString(72, 1285, "MusicBrainz SQL Stories #1")
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


def wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
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
    y: float,
    value: str,
    label: str,
    explanation: str,
) -> None:
    canvas.setFillColor(WHITE)
    canvas.roundRect(72, y, WIDTH - 144, 250, 24, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.roundRect(72, y, 16, 250, 8, fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.setFont("Helvetica-Bold", 74)
    canvas.drawString(120, y + 140, value)
    canvas.setFont("Helvetica-Bold", 28)
    canvas.drawString(120, y + 94, label)
    draw_lines(
        canvas,
        wrap_text(explanation, "Helvetica", 23, 800),
        120,
        y + 55,
        "Helvetica",
        23,
        30,
        MUTED,
    )


def draw_cover(canvas: Canvas) -> None:
    draw_page_base(canvas, 1)
    canvas.setFillColor(ACCENT)
    canvas.roundRect(72, 1090, 235, 44, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawCentredString(189, 1104, "SQL + DATA MODELING")

    draw_lines(
        canvas,
        ["Artist names", "are not identifiers."],
        72,
        930,
        "Helvetica-Bold",
        72,
        86,
    )
    draw_lines(
        canvas,
        [
            "How often does one exact name refer to",
            "several MusicBrainz artist entities?",
        ],
        72,
        690,
        "Helvetica",
        34,
        48,
        MUTED,
    )

    canvas.setFillColor(WHITE)
    canvas.roundRect(72, 300, WIDTH - 144, 235, 24, fill=1, stroke=0)
    canvas.setFillColor(SECONDARY)
    canvas.circle(150, 418, 42, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 30)
    canvas.drawCentredString(150, 407, "2.9M")
    draw_lines(
        canvas,
        ["artist entities", "queried in PostgreSQL"],
        220,
        442,
        "Helvetica-Bold",
        32,
        44,
    )
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 21)
    canvas.drawString(220, 340, "MusicBrainz full export, 2026-07-15")


def draw_scale(canvas: Canvas) -> None:
    draw_page_base(canvas, 2)
    draw_lines(
        canvas,
        ["Two counts,", "two different meanings."],
        72,
        1120,
        "Helvetica-Bold",
        58,
        68,
    )
    draw_metric_card(
        canvas,
        650,
        "126,415",
        "duplicated exact names",
        "Each row of the grouped result represents one name.",
    )
    draw_metric_card(
        canvas,
        330,
        "419,770",
        "artist entities affected",
        "This is the sum of all entities behind those duplicated names.",
    )
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 22)
    canvas.drawString(
        72,
        245,
        "COUNT(*) answers the first question. SUM(entity_count) answers the second.",
    )


def draw_chart(canvas: Canvas) -> None:
    draw_page_base(canvas, 3)
    draw_lines(
        canvas,
        ["One name can hide", "many different entities."],
        72,
        1150,
        "Helvetica-Bold",
        54,
        64,
    )
    canvas.setFillColor(WHITE)
    canvas.roundRect(48, 215, WIDTH - 96, 765, 24, fill=1, stroke=0)
    chart = ImageReader(str(CHART_PATH))
    canvas.drawImage(
        chart,
        70,
        270,
        width=940,
        height=588,
        preserveAspectRatio=True,
        mask="auto",
    )
    canvas.setFillColor(ACCENT)
    canvas.setFont("Helvetica-Bold", 25)
    canvas.drawString(72, 165, "Indigo: 249 artist entities across 52 non-null areas.")


def draw_sql_lesson(canvas: Canvas) -> None:
    draw_page_base(canvas, 4)
    draw_lines(
        canvas,
        ["The SQL is simple.", "The grain is the real lesson."],
        72,
        1120,
        "Helvetica-Bold",
        55,
        66,
    )

    canvas.setFillColor(INK)
    canvas.roundRect(72, 585, WIDTH - 144, 370, 24, fill=1, stroke=0)
    code_lines = [
        "WITH name_counts AS (",
        "  SELECT name, COUNT(*) AS entity_count",
        "  FROM artist",
        "  GROUP BY name",
        "  HAVING COUNT(*) > 1",
        ")",
        "SELECT COUNT(*), SUM(entity_count)",
        "FROM name_counts;",
    ]
    draw_lines(
        canvas,
        code_lines,
        112,
        885,
        "Courier",
        23,
        38,
        WHITE,
    )

    canvas.setFillColor(SECONDARY)
    canvas.roundRect(72, 300, WIDTH - 144, 185, 24, fill=1, stroke=0)
    draw_lines(
        canvas,
        ["A name is an attribute.", "A MusicBrainz ID is an entity key."],
        112,
        412,
        "Helvetica-Bold",
        34,
        50,
        WHITE,
    )
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 23)
    canvas.drawString(72, 225, "Joining on names can silently connect unrelated entities.")


def draw_limits_and_next(canvas: Canvas) -> None:
    draw_page_base(canvas, 5)
    draw_lines(
        canvas,
        ["What this analysis", "does not prove."],
        72,
        1120,
        "Helvetica-Bold",
        58,
        68,
    )

    limitations = [
        "Exact primary names only",
        "Aliases are excluded",
        "[unknown] and [no artist] excluded from the ranking",
        "Catalog coverage is not popularity",
    ]
    y = 850
    for limitation in limitations:
        canvas.setFillColor(ACCENT)
        canvas.circle(92, y + 8, 8, fill=1, stroke=0)
        canvas.setFillColor(INK)
        canvas.setFont("Helvetica", 29)
        canvas.drawString(125, y, limitation)
        y -= 82

    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(2)
    canvas.line(72, 475, WIDTH - 72, 475)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica-Bold", 22)
    canvas.drawString(72, 420, "NEXT EPISODE")
    draw_lines(
        canvas,
        [
            "What happens when artist names",
            "are used as join keys?",
        ],
        72,
        345,
        "Helvetica-Bold",
        40,
        54,
    )
    canvas.setFillColor(SECONDARY)
    canvas.roundRect(72, 170, 385, 54, 27, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawCentredString(264, 188, "MusicBrainz SQL Stories #2")


def build_carousel(output: Path = DEFAULT_OUTPUT) -> Path:
    if not CHART_PATH.is_file():
        raise FileNotFoundError(f"Build the chart first: {CHART_PATH}")

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = Canvas(str(output), pagesize=(WIDTH, HEIGHT))

    for draw_page in [
        draw_cover,
        draw_scale,
        draw_chart,
        draw_sql_lesson,
        draw_limits_and_next,
    ]:
        draw_page(canvas)
        canvas.showPage()

    canvas.save()
    return output


if __name__ == "__main__":
    build_carousel()
