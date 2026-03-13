"""Filesystem paths used by ResearchOS data pipeline."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_PDF_DIR = DATA_DIR / "raw" / "pdf"
INTAKE_RENAMED_DIR = DATA_DIR / "intake" / "renamed"
PARSED_TEXT_DIR = DATA_DIR / "parsed" / "text"


def ensure_data_directories() -> None:
    """Create expected data directories if they do not exist."""
    for path in (RAW_PDF_DIR, INTAKE_RENAMED_DIR, PARSED_TEXT_DIR):
        path.mkdir(parents=True, exist_ok=True)
