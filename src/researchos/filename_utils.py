"""Utilities for deterministic and safe filesystem names."""

from __future__ import annotations

import re
import unicodedata


def normalize_text_for_filename(text: str, max_length: int = 120) -> str:
    """Normalize free text into a readable snake_case-like filename fragment."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    cleaned = ascii_text.lower().strip()
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        cleaned = "untitled"
    return cleaned[:max_length].rstrip("_") or "untitled"


def sanitize_doi_for_filename(doi: str, max_length: int = 120) -> str:
    """Convert DOI into a safe deterministic filename token."""
    value = doi.strip().lower()
    if value.startswith("https://doi.org/"):
        value = value.removeprefix("https://doi.org/")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    if not value:
        value = "unknown_doi"
    return value[:max_length].rstrip("_") or "unknown_doi"
