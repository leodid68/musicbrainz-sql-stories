import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from scripts.build_carousel import HEIGHT, WIDTH, build_carousel


class CarouselTest(unittest.TestCase):
    def test_carousel_has_five_consistent_pages_and_checked_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "carousel.pdf"

            build_carousel(output)

            reader = PdfReader(output)
            self.assertEqual(len(reader.pages), 5)
            for page in reader.pages:
                self.assertAlmostEqual(float(page.mediabox.width), WIDTH)
                self.assertAlmostEqual(float(page.mediabox.height), HEIGHT)

            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )
            for value in [
                "2.93M",
                "5.38M",
                "2,448,276",
                "83.52%",
                "62,001",
                "61,752",
                "controlled self-join",
                "MusicBrainz SQL Stories #2",
            ]:
                self.assertIn(value, text)


if __name__ == "__main__":
    unittest.main()
