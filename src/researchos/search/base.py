"""Base interfaces and shared typing for search adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypedDict


class SearchRecord(TypedDict):
    title: str
    doi: str | None
    year: int | None
    source: str


class SearchAdapter(ABC):
    source_name: str

    @abstractmethod
    def search(self, query: str, limit: int = 5) -> list[SearchRecord]:
        """Return normalized records for a literature source."""
        raise NotImplementedError
