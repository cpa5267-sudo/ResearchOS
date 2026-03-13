from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from researchos.filename_utils import normalize_text_for_filename
from researchos.paper import Paper
from researchos.paper_registry import PaperRegistry
from researchos.pdf_intake import (
    generate_standard_pdf_filename,
    intake_manual_pdfs,
    list_raw_pdf_files,
)


class PdfIntakeTests(unittest.TestCase):
    def test_filename_normalization(self) -> None:
        value = normalize_text_for_filename("Tea Aroma: Volatile Compounds / Review (2024)")
        self.assertEqual(value, "tea_aroma_volatile_compounds_review_2024")

    def test_generates_doi_based_filename_when_doi_exists(self) -> None:
        paper = Paper(title="Any title", doi="10.1021/ACS.JAFc.0c01234", year=2020)
        filename = generate_standard_pdf_filename(paper)
        self.assertEqual(filename, "doi__10_1021_acs_jafc_0c01234.pdf")

    def test_generates_title_year_filename_when_doi_missing(self) -> None:
        paper = Paper(title="Tea Aroma Volatile Compounds Review", doi=None, year=2019)
        filename = generate_standard_pdf_filename(paper)
        self.assertEqual(filename, "tea_aroma_volatile_compounds_review__2019.pdf")

    def test_list_raw_pdf_files_safe_when_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            raw_dir = Path(tmp_dir) / "raw" / "pdf"
            raw_dir.mkdir(parents=True)
            files = list_raw_pdf_files(raw_dir=raw_dir)
        self.assertEqual(files, [])

    def test_manual_intake_moves_pdf_and_updates_pdf_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            raw_dir = root / "raw" / "pdf"
            intake_dir = root / "intake" / "renamed"
            raw_dir.mkdir(parents=True)
            raw_file = raw_dir / "tea_aroma_volatile_compounds_review_source.pdf"
            raw_file.write_bytes(b"%PDF-1.4 test")

            paper = Paper(title="Tea Aroma Volatile Compounds Review", doi=None, year=2019)
            results = intake_manual_pdfs([raw_file], [paper], intake_dir=intake_dir)

            self.assertEqual(len(results), 1)
            self.assertIsNotNone(paper.pdf_path)
            stored_path = Path(paper.pdf_path or "")
            self.assertTrue(stored_path.exists())
            self.assertFalse(raw_file.exists())

    def test_unmatched_pdf_remains_in_raw_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            raw_dir = root / "raw" / "pdf"
            intake_dir = root / "intake" / "renamed"
            raw_dir.mkdir(parents=True)
            raw_file = raw_dir / "unrelated_document.pdf"
            raw_file.write_bytes(b"%PDF-1.4 test")

            paper = Paper(title="Tea Aroma Volatile Compounds Review", doi=None, year=2019)
            results = intake_manual_pdfs([raw_file], [paper], intake_dir=intake_dir)

            self.assertEqual(results, [])
            self.assertTrue(raw_file.exists())
            self.assertIsNone(paper.pdf_path)

    def test_papers_still_missing_pdfs_after_partial_intake(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            raw_dir = root / "raw" / "pdf"
            intake_dir = root / "intake" / "renamed"
            raw_dir.mkdir(parents=True)

            matched_raw = raw_dir / "tea_aroma_volatile_compounds_review.pdf"
            matched_raw.write_bytes(b"%PDF-1.4 test")

            paper1 = Paper(title="Tea Aroma Volatile Compounds Review", year=2019)
            paper2 = Paper(title="Green Tea Polyphenol Stability", year=2020)
            registry = PaperRegistry()
            registry.add(paper1)
            registry.add(paper2)

            intake_manual_pdfs([matched_raw], registry.all(), intake_dir=intake_dir)

            missing = registry.pending_pdf()
            self.assertEqual(len(missing), 1)
            self.assertEqual(missing[0].title, "Green Tea Polyphenol Stability")


if __name__ == "__main__":
    unittest.main()
