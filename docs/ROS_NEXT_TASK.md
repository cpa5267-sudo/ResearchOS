# Next Task

Implement Stage 3 parsing scaffold:
- add a parser module that reads PDFs referenced by `paper.pdf_path`
- write extracted text stubs to `data/parsed/text`
- update paper state (`parsed=True` on success)
- add focused unit tests for parser state transitions and empty-input safety
