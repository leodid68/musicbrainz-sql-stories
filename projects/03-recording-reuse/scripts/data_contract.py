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


def validate_evidence() -> None:
    """Reject inconsistent catalog, outlier, or hierarchy evidence."""
    catalog = load_catalog_summary()
    outlier = load_outlier()
    validation = load_validation()

    if catalog["used_once"] + catalog["used_at_least_twice"] != catalog[
        "recordings_with_tracks"
    ]:
        raise ValueError("catalog reuse counts do not add up")

    if outlier["min_tracks_on_a_medium"] != outlier["max_tracks_on_a_medium"]:
        raise ValueError("outlier has inconsistent tracks per medium")
    if (
        outlier["distinct_mediums"] * outlier["min_tracks_on_a_medium"]
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
