# ROS Status

## Stage 1 — Multi-source search layer
**Status:** Completed

Implemented:
- Source-adapter search package (`openalex`, `crossref`)
- Search manager aggregation and deduplication
- Search loop integration and tests for dedup behavior

## Stage 2a — PDF intake foundation
**Status:** Completed

Implemented:
- Raw PDF discovery (`data/raw/pdf`)
- Deterministic filename utilities
- Intake storage location (`data/intake/renamed`)

## Stage 2b — Manual intake linking
**Status:** Completed (initial/manual matching version)

Implemented:
- Simple raw-PDF to paper matching using normalized filename/title containment
- Matched file move/rename into intake storage
- `paper.pdf_path` updates and intake summary reporting

## Stage 3 — Parsing
**Status:** Not started

Planned:
- Parse PDFs into text artifacts under `data/parsed/text`
- Track parse success/failure states

## Stage 4 — Extraction
**Status:** Not started

Planned:
- Evidence extraction from parsed artifacts
- Structured research-note outputs linked to papers
