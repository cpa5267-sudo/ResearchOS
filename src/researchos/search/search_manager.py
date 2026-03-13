"""Search manager for running and combining multi-source literature queries."""

from __future__ import annotations

from researchos.search.base import SearchAdapter, SearchRecord
from researchos.search.crossref_adapter import CrossrefAdapter
from researchos.search.openalex_adapter import OpenAlexAdapter


def _normalize_title(title: str) -> str:
    return " ".join(title.lower().split())


def _dedupe_records(records: list[SearchRecord]) -> list[SearchRecord]:
    unique: list[SearchRecord] = []
    seen_dois: set[str] = set()
    seen_titles: set[str] = set()

    for record in records:
        doi = (record.get("doi") or "").strip().lower()
        title_key = _normalize_title(record.get("title", "Untitled"))

        if doi and doi in seen_dois:
            continue
        if title_key in seen_titles:
            continue

        unique.append(record)

        if doi:
            seen_dois.add(doi)
        seen_titles.add(title_key)

    return unique


def _get_adapter(source: str) -> SearchAdapter | None:
    adapters: dict[str, SearchAdapter] = {
        "openalex": OpenAlexAdapter(),
        "crossref": CrossrefAdapter(),
    }
    return adapters.get(source)


def search_literature(
    query: str,
    enabled_sources: list[str],
    limit_per_source: int = 5,
) -> tuple[list[SearchRecord], int]:
    merged: list[SearchRecord] = []

    for source in enabled_sources:
        adapter = _get_adapter(source)
        if adapter is None:
            print(f"Unknown search source skipped: {source}")
            continue
        source_records = adapter.search(query, limit=limit_per_source)
        merged.extend(source_records)

    unique_records = _dedupe_records(merged)
    return unique_records, len(merged)
