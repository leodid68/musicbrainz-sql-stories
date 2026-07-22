import unittest
from decimal import Decimal

from scripts.data_contract import (
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
        self.assertEqual(outlier["track_appearances"], 4320)
        self.assertEqual(outlier["distinct_mediums"], 180)
        self.assertEqual(outlier["distinct_releases"], 1)
        self.assertEqual(outlier["min_tracks_on_a_medium"], 24)
        self.assertEqual(outlier["max_tracks_on_a_medium"], 24)
        self.assertEqual(180 * 24, 4320)

    def test_validation_summary(self):
        validation = load_validation()
        self.assertEqual(validation["recording_count"], 3766)
        self.assertEqual(validation["min_track_appearances"], 100)
        self.assertEqual(validation["track_medium_violations"], 0)
        self.assertEqual(validation["medium_release_violations"], 0)
        validate_evidence()


if __name__ == "__main__":
    unittest.main()
