"""Typed loaders and consistency checks for checked recording-reuse exports."""

import csv
from decimal import Decimal
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def _read_single_row(filename: str) -> dict[str, str]:
    with (DATA_DIR / filename).open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))
    if len(rows) != 1:
        raise ValueError(f"{filename} must contain exactly one data row")
    return rows[0]


def load_catalog_summary() -> dict[str, Decimal]:
    """Load the catalog-level metrics without losing decimal precision."""
    return {
        key: Decimal(value)
        for key, value in _read_single_row("catalog-summary.csv").items()
    }


def load_outlier() -> dict[str, str | int]:
    """Load the selected recording's structure, preserving its names as text."""
    row = _read_single_row("outlier-structure.csv")
    name_fields = {"recording_name", "release_name"}
    return {
        key: value if key in name_fields else int(value)
        for key, value in row.items()
    }


def load_validation() -> dict[str, int]:
    """Load the hierarchy-check summary."""
    return {
        key: int(value)
        for key, value in _read_single_row("validation-summary.csv").items()
    }


def _load_high_reuse_recordings() -> list[dict[str, int]]:
    """Load all high-reuse rows to validate the export's row-level evidence."""
    with (DATA_DIR / "high-reuse-recordings.csv").open(
        encoding="utf-8", newline=""
    ) as csv_file:
        return [
            {key: int(value) for key, value in row.items()}
            for row in csv.DictReader(csv_file)
        ]


def validate_evidence() -> None:
    """Reject inconsistent catalog, outlier, or hierarchy evidence."""
    catalog = load_catalog_summary()
    outlier = load_outlier()
    validation = load_validation()
    high_reuse_recordings = _load_high_reuse_recordings()

    if catalog["used_once"] + catalog["used_at_least_twice"] != catalog[
        "recordings_with_tracks"
    ]:
        raise ValueError("catalog reuse counts do not add up")

    if (
        outlier["min_matching_track_rows_per_medium"]
        != outlier["max_matching_track_rows_per_medium"]
    ):
        raise ValueError("outlier has inconsistent matching track rows per medium")
    if (
        outlier["distinct_mediums"]
        * outlier["min_matching_track_rows_per_medium"]
        != outlier["track_appearances"]
    ):
        raise ValueError("outlier track appearances do not match medium arithmetic")
    if not (
        outlier["distinct_releases"]
        <= outlier["distinct_mediums"]
        <= outlier["track_appearances"]
    ):
        raise ValueError("outlier violates release-medium-track hierarchy")
    if validation["track_medium_violations"] or validation[
        "medium_release_violations"
    ]:
        raise ValueError("validation summary reports hierarchy violations")

    if len(high_reuse_recordings) != 3766:
        raise ValueError("high-reuse export must contain 3766 rows")
    if len(high_reuse_recordings) != validation["recording_count"]:
        raise ValueError("high-reuse export row count does not match validation")
    recording_ids = [
        recording["recording_id"] for recording in high_reuse_recordings
    ]
    if len(recording_ids) != len(set(recording_ids)):
        raise ValueError("high-reuse export must contain unique recording IDs")
    expected_order = sorted(
        high_reuse_recordings,
        key=lambda recording: (
            -recording["track_appearances"],
            recording["recording_id"],
        ),
    )
    if high_reuse_recordings != expected_order:
        raise ValueError(
            "high-reuse export must be ordered by track appearances descending "
            "and recording ID ascending"
        )
    minimum_track_appearances = min(
        recording["track_appearances"] for recording in high_reuse_recordings
    )
    if minimum_track_appearances != 100:
        raise ValueError("high-reuse export must start at 100 track appearances")
    if minimum_track_appearances != validation["min_track_appearances"]:
        raise ValueError("high-reuse export minimum does not match validation")
    if any(
        not (
            recording["distinct_releases"]
            <= recording["distinct_mediums"]
            <= recording["track_appearances"]
        )
        for recording in high_reuse_recordings
    ):
        raise ValueError("high-reuse export violates release-medium-track hierarchy")

    leading_recording = high_reuse_recordings[0]
    if (
        leading_recording["recording_id"] != 42361496
        or leading_recording["track_appearances"] != 4320
        or leading_recording["distinct_mediums"] != 180
        or leading_recording["distinct_releases"] != 1
    ):
        raise ValueError("high-reuse export's leading recording is not deterministic")
