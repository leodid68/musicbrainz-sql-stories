import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_chart import build_chart, load_rows


class ChartTest(unittest.TestCase):
    def test_checked_data_is_ranked_and_scoped(self):
        rows = load_rows()

        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[0]["name"], "Indigo")
        self.assertEqual(rows[0]["artist_entities"], 249)
        self.assertEqual(rows[0]["distinct_areas"], 52)
        self.assertNotIn("[unknown]", {row["name"] for row in rows})
        self.assertNotIn("[no artist]", {row["name"] for row in rows})
        self.assertEqual(
            [row["artist_entities"] for row in rows],
            sorted(
                [row["artist_entities"] for row in rows],
                reverse=True,
            ),
        )

    def test_exports_static_and_interactive_versions(self):
        with tempfile.TemporaryDirectory() as directory:
            png = Path(directory) / "chart.png"
            html = Path(directory) / "chart.html"

            build_chart(png_path=png, html_path=html)

            with Image.open(png) as image:
                self.assertEqual(image.size, (1600, 1000))
                self.assertIn(image.mode, {"RGB", "RGBA"})
            self.assertIn("plotly", html.read_text(encoding="utf-8").lower())


if __name__ == "__main__":
    unittest.main()
