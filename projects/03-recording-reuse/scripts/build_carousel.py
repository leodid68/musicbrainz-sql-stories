"""Build and package the five-page recording-reuse PDF carousel."""

from pathlib import Path
from shutil import copyfile

from reportlab.pdfgen import canvas

if __package__:
    from scripts.build_visual import (
        CAROUSEL_DIR,
        PNG_PATH,
        PROJECT_ROOT,
        build_carousel_pages,
    )
else:
    from build_visual import CAROUSEL_DIR, PNG_PATH, PROJECT_ROOT, build_carousel_pages


PDF_PAGE_SIZE = (576, 720)
PDF_TITLE = "MusicBrainz SQL Stories 03 - One Recording, 4,320 Track Rows"
PDF_AUTHOR = "Léo Didier"
PDF_SUBJECT = "SQL grain, track rows, media, and release structure"

PDF_PATH = PROJECT_ROOT / "recording-reuse-carousel.pdf"
PUBLISH_READY_DIR = PROJECT_ROOT / "publish-ready"
PUBLISH_READY_PDF_PATH = PUBLISH_READY_DIR / "recording-reuse-carousel.pdf"
PUBLISH_READY_COVER_PATH = PUBLISH_READY_DIR / "recording-reuse.png"


def build_pdf(page_paths: list[Path], output_path: Path) -> Path:
    """Embed exactly five same-size PNG pages in a PDF."""
    if len(page_paths) != 5:
        raise ValueError("carousel requires exactly five pages")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document = canvas.Canvas(
        str(output_path),
        pagesize=PDF_PAGE_SIZE,
        pageCompression=1,
    )
    document.setTitle(PDF_TITLE)
    document.setAuthor(PDF_AUTHOR)
    document.setSubject(PDF_SUBJECT)
    for page_path in page_paths:
        document.drawImage(
            str(page_path),
            0,
            0,
            width=PDF_PAGE_SIZE[0],
            height=PDF_PAGE_SIZE[1],
            preserveAspectRatio=False,
            mask="auto",
        )
        document.showPage()
    document.save()
    return output_path


def build_carousel() -> tuple[list[Path], Path]:
    """Render pages, build the PDF, and synchronize publication copies."""
    page_paths = build_carousel_pages(CAROUSEL_DIR)
    pdf_path = build_pdf(page_paths, PDF_PATH)
    PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    PUBLISH_READY_DIR.mkdir(parents=True, exist_ok=True)
    copyfile(page_paths[0], PNG_PATH)
    copyfile(page_paths[0], PUBLISH_READY_COVER_PATH)
    copyfile(pdf_path, PUBLISH_READY_PDF_PATH)
    return page_paths, pdf_path


if __name__ == "__main__":
    build_carousel()
