"""OpenAlex source adapter."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from researchos.search.base import SearchAdapter, SearchRecord

OPENALEX_WORKS_URL = "https://api.openalex.org/works"


def _normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    doi = doi.strip()
    if doi.startswith("https://doi.org/"):
        return doi.removeprefix("https://doi.org/")
    return doi


class OpenAlexAdapter(SearchAdapter):
    source_name = "openalex"

    def search(self, query: str, limit: int = 5) -> list[SearchRecord]:
        # OpenAlex official style: `search=<query>` on works endpoint.
        params = urlencode({"search": query, "per-page": max(1, limit)})
        url = f"{OPENALEX_WORKS_URL}?{params}"

        try:
            with urlopen(url, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            print(f"OpenAlex search failed: {exc}")
            return []

        records: list[SearchRecord] = []
        for item in payload.get("results", []):
            records.append(
                {
                    "title": item.get("display_name") or "Untitled",
                    "doi": _normalize_doi(item.get("doi")),
                    "year": item.get("publication_year"),
                    "source": self.source_name,
                }
            )
        return records
