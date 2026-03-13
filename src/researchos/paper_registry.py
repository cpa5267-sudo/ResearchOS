"""Registry for paper records gathered during ROS loop."""

from __future__ import annotations

from researchos.paper import Paper


class PaperRegistry:
    def __init__(self) -> None:
        self._papers: list[Paper] = []

    def add(self, paper: Paper) -> None:
        self._papers.append(paper)

    def all(self) -> list[Paper]:
        return list(self._papers)

    def pending_pdf(self) -> list[Paper]:
        return [paper for paper in self._papers if not paper.pdf_path]

    def pending_parse(self) -> list[Paper]:
        return [paper for paper in self._papers if paper.pdf_path and not paper.parsed]

    def pending_extract(self) -> list[Paper]:
        return [paper for paper in self._papers if paper.parsed and not paper.extracted]
