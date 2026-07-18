import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from scripts.build_carousel import build_carousel


class CarouselTest(unittest.TestCase):
    def test_carousel_has_five_pages_and_checked_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "carousel.pdf"

            build_carousel(output)

            reader = PdfReader(output)
            self.assertEqual(len(reader.pages), 5)
            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )
            for value in [
                "126,415",
                "419,770",
                "Indigo",
                "249",
                "MusicBrainz ID",
            ]:
                self.assertIn(value, text)


if __name__ == "__main__":
    unittest.main()
