# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **research repository** (not a software product): a verified literature survey plus a research proposal on *runtime autotuning of production LLM inference frameworks* (vLLM V1 and SGLang). There is no application to build. The deliverables are prose documents backed by downloaded papers and audit artifacts. There is no git repository here.

The two primary documents are written in **Chinese**; match that language when editing them. The `scripts/` tooling and `evidence/*.json` are in English.

## Layout

- `01_顶会论文调研.md` — literature survey: 17 verified top-venue papers, relevance table, close-reading notes. Each paper reference separates publication identity from the downloaded version.
- `02_研究方案.md` — research proposal: what vLLM/SGLang natively support vs. what must be built for safe online (hot) parameter control. Ends with `[V1]`/`[S1]` reference-link definitions pinned to fixed upstream commits.
- `papers.json` — manifest of record: per-paper id, venue, URLs, `file`, `status`, `bytes`, `sha256`, version notes, download attempts.
- `papers/` and `paper-text/` — downloaded PDFs and their PDFKit-extracted text (page-boundary-preserving, `NN_Name.pdf` ↔ `NN_Name.txt`).
- `references.bib` — one BibTeX entry per paper (count must equal `papers.json`).
- `evidence/` — append-only audit JSONs with timestamps, file SHA-256s, and explicit scope disclaimers (e.g. `source-audit-2026-11-01.json`, `framework-parameter-inventory-*.json`). These record read-only source audits of local vLLM/SGLang checkouts at pinned commits; no framework code was modified.

## Commands

All commands run from the repository root (the extractor writes into `./paper-text/`).

```bash
# Download/repair PDFs listed in papers.json (all, or selected ids); updates the manifest.
python3 scripts/download_papers.py            # all
python3 scripts/download_papers.py 07 12      # specific paper ids

# Range-download a single large PDF when a slow connection times out.
python3 scripts/download_ranges.py URL BYTE_LENGTH papers/NN_Name.pdf

# Rebuild the extractor (prebuilt binary scripts/extract_pdf is checked in), then extract text.
swiftc scripts/extract_pdf.swift -o scripts/extract_pdf
./scripts/extract_pdf papers/*.pdf

# Validate all offline artifacts; rewrites evidence/validation.json. Exits non-zero on any error.
python3 scripts/validate_research.py
```

`validate_research.py` is the project's test suite. It checks, per paper, PDF header/EOF, that `bytes`/`sha256` match the manifest, parsed page count > 0, page-marker count matches, and text present; globally it checks that every relative Markdown link resolves and that the BibTeX entry count equals the paper count. **Run it after touching any paper, manifest entry, Markdown relative link, or bib entry.**

## Conventions that matter (evidence discipline)

This project's whole value is provenance rigor. Preserve it:

- **Never invent or alter a number, hash, date, or claim.** Figures come only from the cited artifact. Keep `papers.json` sha256/bytes consistent with the actual files — the download script sets them; don't hand-edit to make validation pass.
- **Separate publication identity from downloaded version.** A paper can be accepted at a venue while the local PDF is an author arXiv version with *different* experimental numbers (e.g. TuxBot). Bind any quoted number to the specific version; never splice numbers across versions.
- **Separate "native capability" from "proposed, unimplemented extension."** In `02_研究方案.md` and the audits, framework parameters are labeled as exposing existing policy, needing a new state-update protocol, or being a new algorithm. Do not describe proposed research interfaces as if the frameworks already support them.
- **Source links are pinned to fixed commits.** vLLM/SGLang references use the commit SHAs recorded in `source-audit-2026-11-01.json`; keep `[V*]`/`[S*]` link targets on those commits unless deliberately re-auditing.
- **State limits honestly.** "Not found in this screening" is not "does not exist." No GPU/inference results exist yet; audits are read-only. Keep the scope disclaimers.
- When adding a paper: add to `papers.json`, download, extract text, add a `references.bib` entry, cite it in the survey, then run the validator so counts and links stay consistent.
