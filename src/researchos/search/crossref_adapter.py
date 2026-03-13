"""Crossref source adapter."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from researchos.search.base import SearchAdapter, SearchRecord

CROSSREF_WORKS_URL = "https://api.crossref.org/works"


def _normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    return doi.strip().removeprefix("https://doi.org/").lower()


class CrossrefAdapter(SearchAdapter):
    source_name = "crossref"

    def search(self, query: str, limit: int = 5) -> list[SearchRecord]:
        params = urlencode({"query": query, "rows": max(1, limit)})
        url = f"{CROSSREF_WORKS_URL}?{params}"

        try:
            with urlopen(url, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            print(f"Crossref search failed: {exc}")
            return []

        items = payload.get("message", {}).get("items", [])
        records: list[SearchRecord] = []
        for item in items:
            titles = item.get("title") or []
            published = item.get("issued", {}).get("date-parts", [[None]])
            year = published[0][0] if published and published[0] else None
            records.append(
                {
                    "title": (titles[0] if titles else "Untitled"),
                    "doi": _normalize_doi(item.get("DOI")),
                    "year": year,
                    "source": self.source_name,
                }
            )
        return records
