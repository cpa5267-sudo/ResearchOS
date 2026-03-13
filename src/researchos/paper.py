"""Paper domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Paper:
    title: str
    doi: str | None = None
    year: int | None = None
    authors: list[str] | None = None
    pdf_path: str | None = None
    parsed: bool = False
    extracted: bool = False
    notes: str | None = None
