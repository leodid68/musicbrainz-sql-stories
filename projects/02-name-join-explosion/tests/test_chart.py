import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_chart import build_chart, load_metrics


class ChartTest(unittest.TestCase):
    def test_checked_metrics_match_the_sql_claims(self):
        metrics = load_metrics()

        self.assertEqual(metrics["original_artist_rows"], 2_931_345)
        self.assertEqual(metrics["name_join_rows"], 5_379_621)
        self.assertEqual(metrics["cross_entity_matches"], 2_448_276)
        self.assertEqual(metrics["row_increase_pct"], 83.52)
        self.assertEqual(metrics["indigo_entities"], 249)
        self.assertEqual(metrics["indigo_name_join_rows"], 62_001)
        self.assertEqual(metrics["indigo_cross_entity_matches"], 61_752)
        self.assertEqual(
            metrics["name_join_rows"] - metrics["original_artist_rows"],
            metrics["cross_entity_matches"],
        )

    def test_exports_static_and_interactive_chart(self):
        with tempfile.TemporaryDirectory() as directory:
            png = Path(directory) / "name-join-impact.png"
            html = Path(directory) / "name-join-impact.html"

            build_chart(png_path=png, html_path=html)

            with Image.open(png) as image:
                self.assertEqual(image.size, (1600, 1000))
                self.assertIn(image.mode, {"RGB", "RGBA"})
            html_text = html.read_text(encoding="utf-8").lower()
            self.assertIn("plotly", html_text)
            self.assertIn("83.52%", html_text)


if __name__ == "__main__":
    unittest.main()
