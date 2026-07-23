import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from scripts.build_carousel import build_pdf
from scripts.build_visual import build_carousel_pages


class CarouselPdfTest(unittest.TestCase):
    def test_pdf_has_five_equal_pages_and_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            pages = build_carousel_pages(directory / "pages")
            pdf = build_pdf(pages, directory / "carousel.pdf")
            reader = PdfReader(pdf)

            self.assertEqual(len(reader.pages), 5)
            self.assertEqual(
                {
                    (float(page.mediabox.width), float(page.mediabox.height))
                    for page in reader.pages
                },
                {(576.0, 720.0)},
            )
            self.assertEqual(
                reader.metadata.title,
                "MusicBrainz SQL Stories 03 - One Recording, 4,320 Track Rows",
            )
            self.assertEqual(reader.metadata.author, "Léo Didier")
            self.assertEqual(
                reader.metadata.subject,
                "SQL grain, track rows, media, and release structure",
            )
            self.assertLess(pdf.stat().st_size, 100 * 1024 * 1024)

    def test_pdf_rejects_any_page_count_other_than_five(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "carousel.pdf"
            with self.assertRaisesRegex(ValueError, "exactly five pages"):
                build_pdf([], output)


if __name__ == "__main__":
    unittest.main()
