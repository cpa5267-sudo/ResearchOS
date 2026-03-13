"""Manual PDF intake foundation for ResearchOS."""

from __future__ import annotations

from pathlib import Path
import shutil

from researchos.filename_utils import normalize_text_for_filename, sanitize_doi_for_filename
from researchos.paper import Paper
from researchos.paths import INTAKE_RENAMED_DIR, RAW_PDF_DIR


def list_raw_pdf_files(raw_dir: Path = RAW_PDF_DIR) -> list[Path]:
    """List raw PDFs available for intake."""
    if not raw_dir.exists():
        return []
    return sorted(path for path in raw_dir.iterdir() if path.is_file() and path.suffix.lower() == ".pdf")


def generate_standard_pdf_filename(paper: Paper) -> str:
    """Generate deterministic intake filename for a paper."""
    if paper.doi:
        stem = sanitize_doi_for_filename(paper.doi)
        return f"doi__{stem}.pdf"

    title_part = normalize_text_for_filename(paper.title)
    year_part = str(paper.year) if paper.year is not None else "unknown_year"
    return f"{title_part}__{year_part}.pdf"


def move_raw_pdf_to_intake(raw_pdf_path: Path, paper: Paper, intake_dir: Path = INTAKE_RENAMED_DIR) -> Path:
    """Move a raw PDF into intake with standardized naming and update paper path."""
    intake_dir.mkdir(parents=True, exist_ok=True)
    destination = intake_dir / generate_standard_pdf_filename(paper)

    if destination.exists():
        stem, suffix = destination.stem, destination.suffix
        counter = 2
        while destination.exists():
            destination = intake_dir / f"{stem}__{counter}{suffix}"
            counter += 1

    shutil.move(str(raw_pdf_path), str(destination))
    paper.pdf_path = str(destination)
    return destination


def intake_raw_pdf(raw_pdf_path: Path, paper: Paper) -> dict:
    """Run manual intake for one raw PDF and return summary record."""
    destination = move_raw_pdf_to_intake(raw_pdf_path, paper)
    return {
        "raw_pdf": str(raw_pdf_path),
        "stored_pdf": str(destination),
        "paper_title": paper.title,
        "paper_doi": paper.doi,
    }
