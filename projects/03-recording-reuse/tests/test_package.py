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
EPISODE_TWO_URL = (
    "https://www.linkedin.com/posts/"
    "leodidierfr_sql-stories-p2-ugcPost-7484575799333875712-oHDE"
)


class EditorialPackageTests(unittest.TestCase):
    def read_public_files(self):
        texts = {}
        for filename in PUBLIC_FILES:
            path = PROJECT_ROOT / filename
            self.assertTrue(path.is_file(), f"missing public file: {filename}")
            texts[filename] = path.read_text(encoding="utf-8")
        return texts

    def read_project_block(self, root_readme, episode_number):
        marker = f"### [{episode_number:02d}."
        start = root_readme.index(marker)
        end = root_readme.find("\n### ", start + len(marker))
        if end == -1:
            end = root_readme.find("\n## ", start + len(marker))
        return root_readme[start:end]

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
        self.assertIn("18.84%", linkedin_text)
        self.assertNotIn("18.8357465370108153%", linkedin_text)
        self.assertIn("have at least two track rows", linkedin_text)

    def test_root_index_links_current_series_statuses(self):
        root_readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        episode_two = self.read_project_block(root_readme, 2)
        episode_three = self.read_project_block(root_readme, 3)

        self.assertIn("projects/02-name-join-explosion/", episode_two)
        self.assertIn("Status: Published.", episode_two)
        self.assertIn("Published: 22 July 2026", episode_two)
        self.assertIn(EPISODE_TWO_URL, episode_two)
        self.assertNotIn("Draft for review", episode_two)

        self.assertIn("projects/03-recording-reuse/", episode_three)
        self.assertIn("Status: Draft for review.", episode_three)
        self.assertNotIn("Status: Published.", episode_three)

    def test_episode_two_publication_notes_preserve_published_history(self):
        notes_path = (
            REPOSITORY_ROOT
            / "projects/02-name-join-explosion/publish-ready/publication-notes.md"
        )
        notes = notes_path.read_text(encoding="utf-8")

        self.assertIn("Status: published", notes)
        self.assertIn("Published: 22 July 2026", notes)
        self.assertIn(EPISODE_TWO_URL, notes)
        self.assertNotIn("No LinkedIn publication URL exists yet", notes)


if __name__ == "__main__":
    unittest.main()
