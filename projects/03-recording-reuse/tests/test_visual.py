import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.build_visual import build_visual, medium_positions


class VisualTest(unittest.TestCase):
    def test_medium_grid_contains_exactly_180_symbols(self):
        positions = medium_positions()
        self.assertEqual(len(positions), 180)
        self.assertEqual(len(set(positions)), 180)

    def test_visual_exports_expected_portrait_png(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "recording-reuse.png"
            build_visual(output)
            with Image.open(output) as image:
                self.assertEqual(image.size, (1200, 1500))
                self.assertIn(image.mode, {"RGB", "RGBA"})


if __name__ == "__main__":
    unittest.main()
