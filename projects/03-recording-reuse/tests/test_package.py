import re
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
PUBLISH_READY_FILES = (
    "README.md",
    "accessibility.txt",
    "claim-ledger.md",
    "linkedin-post.txt",
    "publication-notes.md",
    "recording-reuse.png",
)
CANONICAL_CLAIMS_BY_FILE = {
    "README.md": (
        "39,332,638",
        "56,818,950",
        "18.8357465370108153%",
        "3,766",
        "4,320 track rows",
        "one release",
        "180 media",
        "24 matching track rows per medium",
    ),
    "claim-ledger.md": (
        "39,332,638",
        "56,818,950",
        "18.8357465370108153%",
        "3,766",
        "4,320 track rows",
        "one release",
        "180 distinct media",
        "24 matching track rows",
    ),
    "data-post-brief.md": (
        "39,332,638",
        "56,818,950",
        "18.8357465370108153%",
        "3,766",
        "4,320 track rows",
        "one release",
        "180 media",
        "24 matching track rows per medium",
    ),
    "linkedin-post.md": (
        "39,332,638",
        "7,408,596",
        "18.84%",
        "3,766",
        "4,320 track rows",
        "single release",
        "180 media",
        "24 matching track rows",
    ),
    "accessibility.md": (
        "4,320 track rows",
        "one release",
        "180",
        "24 matching track rows",
        "COUNT(track.id)",
        "COUNT(DISTINCT release.id)",
    ),
}


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

    def test_canonical_claims_appear_in_their_intended_artifacts(self):
        public_texts = self.read_public_files()

        for filename, claims in CANONICAL_CLAIMS_BY_FILE.items():
            normalized_text = " ".join(public_texts[filename].split())
            for claim in claims:
                with self.subTest(filename=filename, claim=claim):
                    self.assertIn(claim, normalized_text)

    def test_analysis_uses_only_temp_schema_qualified_cleanup(self):
        analysis_sql = (PROJECT_ROOT / "analysis.sql").read_text(encoding="utf-8")
        drop_targets = re.findall(
            r"DROP\s+TABLE\s+IF\s+EXISTS\s+([^\s;]+)",
            analysis_sql,
            flags=re.IGNORECASE,
        )

        unsafe_targets = [
            target for target in drop_targets if not target.startswith("pg_temp.")
        ]
        self.assertEqual(
            unsafe_targets,
            [],
            f"unsafe DROP targets: {unsafe_targets}",
        )

    def test_outlier_sql_counts_matching_rows_at_medium_grain(self):
        analysis_sql = (PROJECT_ROOT / "analysis.sql").read_text(encoding="utf-8")
        checks_sql = (PROJECT_ROOT / "checks.sql").read_text(encoding="utf-8")

        for filename, sql_text in (
            ("analysis.sql", analysis_sql),
            ("checks.sql", checks_sql),
        ):
            with self.subTest(filename=filename):
                self.assertIn("outlier_medium_usage AS", sql_text)
                self.assertIn(
                    "COUNT(track.id) AS matching_track_rows",
                    sql_text,
                )
                self.assertIn(
                    "MIN(matching_track_rows)",
                    sql_text,
                )
                self.assertIn(
                    "MAX(matching_track_rows)",
                    sql_text,
                )
                self.assertNotIn("medium.track_count", sql_text)

        self.assertIn(
            "SUM(matching_track_rows) AS track_appearances",
            analysis_sql,
        )
        self.assertIn(
            "MIN(matching_track_rows) AS min_matching_track_rows_per_medium",
            analysis_sql,
        )
        self.assertIn(
            "MAX(matching_track_rows) AS max_matching_track_rows_per_medium",
            analysis_sql,
        )

    def test_readme_reproduces_exports_and_visual_from_explicit_directories(self):
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("From the repository root", readme)
        self.assertIn(
            "-f projects/03-recording-reuse/export.sql",
            readme,
        )
        self.assertIn("cd projects/03-recording-reuse", readme)
        self.assertIn(
            "../../.venv/bin/python scripts/build_visual.py",
            readme,
        )

    def test_linkedin_final_copy_uses_checked_claims_and_cte(self):
        linkedin_text = self.read_public_files()["linkedin-post.md"]

        self.assertNotIn("editable draft", linkedin_text.lower())
        self.assertNotIn("popularity", linkedin_text.lower())
        self.assertNotIn("—", linkedin_text)
        self.assertLessEqual(linkedin_text.count("🎧"), 1)
        self.assertIn("18.84%", linkedin_text)
        self.assertNotIn("18.8357465370108153%", linkedin_text)
        self.assertIn("have at least two track rows", linkedin_text)
        self.assertIn("Only 3,766 have at least 100 track rows.", linkedin_text)
        self.assertIn("WITH recording_usage AS (", linkedin_text)
        self.assertIn("GROUP BY track.recording", linkedin_text)
        self.assertIn("This CTE returns one row per recording", linkedin_text)
        self.assertIn("COUNT(DISTINCT release.id)", linkedin_text)

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
        self.assertIn(
            "Status: Draft — final text approved; visual review pending.",
            episode_three,
        )
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

    def test_publish_ready_bundle_contains_approved_text_and_draft_status(self):
        publish_ready = PROJECT_ROOT / "publish-ready"

        for filename in PUBLISH_READY_FILES:
            self.assertTrue(
                (publish_ready / filename).is_file(),
                f"missing publish-ready file: {filename}",
            )

        self.assertEqual(
            (publish_ready / "recording-reuse.png").read_bytes(),
            (PROJECT_ROOT / "charts/recording-reuse.png").read_bytes(),
        )
        self.assertEqual(
            (publish_ready / "linkedin-post.txt").read_text(encoding="utf-8"),
            (PROJECT_ROOT / "linkedin-post.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            (publish_ready / "accessibility.txt").read_bytes(),
            (PROJECT_ROOT / "accessibility.md").read_bytes(),
        )
        self.assertEqual(
            (publish_ready / "claim-ledger.md").read_bytes(),
            (PROJECT_ROOT / "claim-ledger.md").read_bytes(),
        )
        notes = (publish_ready / "publication-notes.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Status: draft; final text approved by Leo on 23 July 2026, "
            "visual review pending.",
            notes,
        )


if __name__ == "__main__":
    unittest.main()
