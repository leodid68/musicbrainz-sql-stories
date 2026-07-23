import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import build_visual as visual
from scripts.build_visual import (
    build_visual,
    carousel_page_paths,
    medium_positions,
    track_marker_positions,
)


class VisualTest(unittest.TestCase):
    def test_medium_grid_contains_exactly_180_symbols(self):
        positions = medium_positions()
        self.assertEqual(len(positions), 180)
        self.assertEqual(len(set(positions)), 180)

    def test_each_medium_contains_exactly_24_track_markers(self):
        markers = track_marker_positions()
        self.assertEqual(len(markers), 24)
        self.assertEqual(len(set(markers)), 24)
        self.assertEqual(len(medium_positions()) * len(markers), 4320)

    def test_carousel_has_five_stable_page_names(self):
        paths = carousel_page_paths(Path("/tmp/carousel"))
        self.assertEqual(
            [path.name for path in paths],
            [
                "page-01-hook.png",
                "page-02-reveal.png",
                "page-03-structure.png",
                "page-04-sql.png",
                "page-05-lesson.png",
            ],
        )

    def test_visual_exports_expected_portrait_png(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "recording-reuse.png"
            build_visual(output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1200, 1500))
                self.assertIn(image.mode, {"RGB", "RGBA"})

    def test_required_supporting_text_is_legible_at_feed_scale(self):
        sizes = visual.supporting_text_sizes()
        self.assertEqual(
            set(sizes),
            {"sql_method", "snapshot", "catalog_limit"},
        )
        self.assertGreaterEqual(min(sizes.values()) * 0.30, 8)


if __name__ == "__main__":
    unittest.main()
