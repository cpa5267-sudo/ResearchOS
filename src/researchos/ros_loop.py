"""Core ROS loop orchestration."""

from __future__ import annotations

from researchos.paper import Paper
from researchos.paper_registry import PaperRegistry
from researchos.paths import ensure_data_directories
from researchos.pdf_intake import list_raw_pdf_files
from researchos.search.search_manager import search_literature


class ROSLoop:
    def __init__(self, research_question: str) -> None:
        self.research_question = research_question
        self.registry = PaperRegistry()

    def search(self) -> list[dict]:
        enabled_sources = ["openalex", "crossref"]
        print(f"Running literature search (sources: {', '.join(enabled_sources)})")

        unique_records, total_before_dedup = search_literature(
            self.research_question,
            enabled_sources=enabled_sources,
        )

        print(f"Results before deduplication: {total_before_dedup}")
        print(f"Unique papers after deduplication: {len(unique_records)}")
        return unique_records

    def run(self) -> None:
        ensure_data_directories()

        records = self.search()
        for record in records:
            self.registry.add(
                Paper(
                    title=record.get("title", "Untitled"),
                    doi=record.get("doi"),
                    year=record.get("year"),
                )
            )

        raw_pdfs = list_raw_pdf_files()

        print(f"Registered papers: {len(self.registry.all())}")
        print(f"Raw PDFs detected: {len(raw_pdfs)}")
        print(f"Papers missing PDFs: {len(self.registry.pending_pdf())}")
        print(f"Pending PDFs: {len(self.registry.pending_pdf())}")
        print(f"Pending parse: {len(self.registry.pending_parse())}")
        print(f"Pending extract: {len(self.registry.pending_extract())}")
