"""Backward-compatible OpenAlex search wrapper."""

from __future__ import annotations

from researchos.search.openalex_adapter import OpenAlexAdapter


def search_openalex(query: str, limit: int = 5) -> list[dict]:
    """Search OpenAlex works and return normalized records."""
    return OpenAlexAdapter().search(query, limit=limit)
