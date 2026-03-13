from __future__ import annotations

import unittest
from unittest.mock import patch

from researchos.search.base import SearchAdapter
from researchos.search.search_manager import search_literature


class _FakeAdapter(SearchAdapter):
    def __init__(self, source_name: str, records: list[dict]) -> None:
        self.source_name = source_name
        self._records = records

    def search(self, query: str, limit: int = 5) -> list[dict]:
        return self._records[:limit]


class SearchManagerTests(unittest.TestCase):
    def test_deduplicates_by_doi(self) -> None:
        openalex_records = [
            {"title": "Paper A", "doi": "10.1000/abc", "year": 2023, "source": "openalex"},
        ]
        crossref_records = [
            {
                "title": "Paper A (duplicate)",
                "doi": "10.1000/ABC",
                "year": 2024,
                "source": "crossref",
            },
        ]

        fake_adapters = {
            "openalex": _FakeAdapter("openalex", openalex_records),
            "crossref": _FakeAdapter("crossref", crossref_records),
        }

        with patch("researchos.search.search_manager._get_adapter", side_effect=fake_adapters.get):
            unique, total = search_literature("q", ["openalex", "crossref"])

        self.assertEqual(total, 2)
        self.assertEqual(len(unique), 1)
        self.assertEqual(unique[0]["doi"].lower(), "10.1000/abc")

    def test_deduplicates_missing_doi_by_normalized_title(self) -> None:
        openalex_records = [
            {"title": "A  Great Paper", "doi": None, "year": 2023, "source": "openalex"},
        ]
        crossref_records = [
            {"title": "a great paper", "doi": None, "year": 2022, "source": "crossref"},
        ]

        fake_adapters = {
            "openalex": _FakeAdapter("openalex", openalex_records),
            "crossref": _FakeAdapter("crossref", crossref_records),
        }

        with patch("researchos.search.search_manager._get_adapter", side_effect=fake_adapters.get):
            unique, total = search_literature("q", ["openalex", "crossref"])

        self.assertEqual(total, 2)
        self.assertEqual(len(unique), 1)
        self.assertEqual(unique[0]["title"], "A  Great Paper")

    def test_deduplicates_same_title_when_only_one_record_has_doi(self) -> None:
        openalex_records = [
            {"title": "Tea Aroma Chemistry", "doi": "10.1000/tea.1", "year": 2021, "source": "openalex"},
        ]
        crossref_records = [
            {"title": "tea   aroma chemistry", "doi": None, "year": 2021, "source": "crossref"},
        ]

        fake_adapters = {
            "openalex": _FakeAdapter("openalex", openalex_records),
            "crossref": _FakeAdapter("crossref", crossref_records),
        }

        with patch("researchos.search.search_manager._get_adapter", side_effect=fake_adapters.get):
            unique, total = search_literature("q", ["openalex", "crossref"])

        self.assertEqual(total, 2)
        self.assertEqual(len(unique), 1)
        self.assertEqual(unique[0]["title"], "Tea Aroma Chemistry")


if __name__ == "__main__":
    unittest.main()
