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


def intake_raw_pdf(raw_pdf_path: Path, paper: Paper, intake_dir: Path = INTAKE_RENAMED_DIR) -> dict:
    """Run manual intake for one raw PDF and return summary record."""
    destination = move_raw_pdf_to_intake(raw_pdf_path, paper, intake_dir=intake_dir)
    return {
        "raw_pdf": str(raw_pdf_path),
        "stored_pdf": str(destination),
        "paper_title": paper.title,
        "paper_doi": paper.doi,
    }


def _matches_raw_pdf_to_paper(raw_pdf_path: Path, paper: Paper) -> bool:
    raw_stem = normalize_text_for_filename(raw_pdf_path.stem)
    paper_title = normalize_text_for_filename(paper.title)

    if not paper_title:
        return False

    return paper_title in raw_stem or raw_stem in paper_title


def intake_manual_pdfs(
    raw_pdf_paths: list[Path],
    papers: list[Paper],
    intake_dir: Path = INTAKE_RENAMED_DIR,
) -> list[dict]:
    """Attempt simple filename/title-based matching and intake for raw PDFs."""
    results: list[dict] = []

    for raw_pdf in raw_pdf_paths:
        matched_paper: Paper | None = None

        for paper in papers:
            if paper.pdf_path:
                continue
            if _matches_raw_pdf_to_paper(raw_pdf, paper):
                matched_paper = paper
                break

        if matched_paper is None:
            continue

        results.append(intake_raw_pdf(raw_pdf, matched_paper, intake_dir=intake_dir))

    return results
