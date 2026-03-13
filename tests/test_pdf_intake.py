from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from researchos.filename_utils import normalize_text_for_filename
from researchos.paper import Paper
from researchos.pdf_intake import generate_standard_pdf_filename, list_raw_pdf_files


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


if __name__ == "__main__":
    unittest.main()
