import unittest
from copy import deepcopy
from decimal import Decimal
from unittest.mock import patch

from scripts.data_contract import (
    _load_high_reuse_recordings,
    load_catalog_summary,
    load_outlier,
    load_validation,
    validate_evidence,
)


class DataContractTest(unittest.TestCase):
    def test_checked_catalog_metrics(self):
        metrics = load_catalog_summary()
        self.assertEqual(metrics["recordings_with_tracks"], Decimal("39332638"))
        self.assertEqual(metrics["total_track_appearances"], Decimal("56818950"))
        self.assertEqual(metrics["used_once"], Decimal("31924042"))
        self.assertEqual(metrics["used_at_least_twice"], Decimal("7408596"))
        self.assertEqual(metrics["used_at_least_10"], Decimal("244908"))
        self.assertEqual(metrics["used_at_least_100"], Decimal("3766"))
        self.assertEqual(metrics["reuse_share_pct"], Decimal("18.8357465370108153"))

    def test_outlier_arithmetic_and_hierarchy(self):
        outlier = load_outlier()
        self.assertEqual(outlier["recording_id"], 42361496)
        self.assertEqual(
            outlier["recording_name"],
            "I Feel Bad For Your Hard Drive",
        )
        self.assertEqual(outlier["release_id"], 5055218)
        self.assertEqual(outlier["release_name"], "I Feel Bad For Your Hard Drive")
        self.assertEqual(outlier["track_appearances"], 4320)
        self.assertEqual(outlier["distinct_mediums"], 180)
        self.assertEqual(outlier["distinct_releases"], 1)
        self.assertEqual(outlier["min_matching_track_rows_per_medium"], 24)
        self.assertEqual(outlier["max_matching_track_rows_per_medium"], 24)
        self.assertNotIn("min_tracks_on_a_medium", outlier)
        self.assertNotIn("max_tracks_on_a_medium", outlier)
        self.assertEqual(180 * 24, 4320)

    def test_high_reuse_export_matches_checked_hierarchy(self):
        recordings = _load_high_reuse_recordings()

        self.assertEqual(len(recordings), 3766)
        self.assertEqual(recordings[0]["recording_id"], 42361496)
        self.assertEqual(recordings[0]["track_appearances"], 4320)
        self.assertEqual(recordings[0]["distinct_mediums"], 180)
        self.assertEqual(recordings[0]["distinct_releases"], 1)
        self.assertEqual(
            min(recording["track_appearances"] for recording in recordings), 100
        )
        self.assertTrue(
            all(
                recording["distinct_releases"]
                <= recording["distinct_mediums"]
                <= recording["track_appearances"]
                for recording in recordings
            )
        )
        self.assertEqual(
            len({recording["recording_id"] for recording in recordings}),
            len(recordings),
        )
        self.assertEqual(
            recordings,
            sorted(
                recordings,
                key=lambda recording: (
                    -recording["track_appearances"],
                    recording["recording_id"],
                ),
            ),
        )

    def test_validation_rejects_duplicate_high_reuse_recording_ids(self):
        recordings = deepcopy(_load_high_reuse_recordings())
        recordings[1]["recording_id"] = recordings[0]["recording_id"]

        with patch(
            "scripts.data_contract._load_high_reuse_recordings",
            return_value=recordings,
        ):
            with self.assertRaisesRegex(ValueError, "unique recording IDs"):
                validate_evidence()

    def test_validation_rejects_incomplete_high_reuse_ordering(self):
        recordings = deepcopy(_load_high_reuse_recordings())
        recordings[1], recordings[2] = recordings[2], recordings[1]

        with patch(
            "scripts.data_contract._load_high_reuse_recordings",
            return_value=recordings,
        ):
            with self.assertRaisesRegex(
                ValueError,
                "track appearances descending and recording ID ascending",
            ):
                validate_evidence()

    def test_validation_summary(self):
        validation = load_validation()
        self.assertEqual(validation["recording_count"], 3766)
        self.assertEqual(validation["min_track_appearances"], 100)
        self.assertEqual(validation["track_medium_violations"], 0)
        self.assertEqual(validation["medium_release_violations"], 0)
        validate_evidence()


if __name__ == "__main__":
    unittest.main()
