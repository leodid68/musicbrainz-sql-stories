import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parents[1]
PUBLIC_FILES = (
    "README.md",
    "claim-ledger.md",
    "data-post-brief.md",
    "linkedin-post.md",
    "accessibility.md",
)


class EditorialPackageTests(unittest.TestCase):
    def read_public_files(self):
        texts = {}
        for filename in PUBLIC_FILES:
            path = PROJECT_ROOT / filename
            self.assertTrue(path.is_file(), f"missing public file: {filename}")
            texts[filename] = path.read_text(encoding="utf-8")
        return texts

    def test_public_files_include_checked_claims_and_sql_method(self):
        combined_public_text = "\n".join(self.read_public_files().values())

        required_claims = [
            "39,332,638",
            "56,818,950",
            "18.8357465370108153%",
            "3,766",
            "4,320",
            "180",
            "24",
            "one release",
        ]
        for claim in required_claims:
            self.assertIn(claim, combined_public_text)

        self.assertIn("COUNT(track.id)", combined_public_text)
        self.assertIn("COUNT(DISTINCT release.id)", combined_public_text)
        self.assertIn("catalog", combined_public_text.lower())

    def test_linkedin_draft_avoids_unsupported_or_overpolished_copy(self):
        linkedin_text = self.read_public_files()["linkedin-post.md"]

        self.assertIn("draft", linkedin_text.lower())
        self.assertIn("Leo", linkedin_text)
        self.assertNotIn("popularity", linkedin_text.lower())
        self.assertNotIn("—", linkedin_text)
        self.assertLessEqual(linkedin_text.count("🎧"), 1)

    def test_root_index_links_current_series_statuses(self):
        root_readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("projects/02-name-join-explosion/", root_readme)
        self.assertIn("projects/03-recording-reuse/", root_readme)
        self.assertIn("Draft for review", root_readme)


if __name__ == "__main__":
    unittest.main()
