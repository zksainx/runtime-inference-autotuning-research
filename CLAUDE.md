# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **research repository** (not a software product): a verified literature survey plus two research designs on *runtime autotuning of production LLM inference frameworks* (vLLM V1 and SGLang). There is no application to build. The deliverables are prose documents backed by downloaded papers and audit artifacts. No framework code has been modified and no GPU experiments have been run yet.

The survey and two research designs are written in **Chinese**; match that language when editing them. The `scripts/` tooling and `evidence/*.json` are in English.

## Layout

- `01_顶会论文调研.md` — literature survey: two major parts corresponding to the shadow-optimization proposal (Part I) and the independent PD-elasticity design (Part II). Part I retains 17 verified venue papers, the detailed Herschel/Autopoiesis/FlashVector v1 readings in §1.4 and related preprints in §1.7. Part II adds 13 papers (ids 21–33), with focused mechanism readings and a feature matrix. Across the two parts, 25 unique venue/program identities are independently confirmed, including TaiChi in the future SC 2026 program (2026-11-18); 8 author/preprint or unresolved-publication entries are kept separate. §2.7–2.8 contain shared artifacts. Each reference separates publication identity from the downloaded version.
- `02_研究方案_MaaS影子实验与持续自优化.md` — main research proposal: production observation, shadow-traffic experiments, fast configuration/policy tuning and slow code/kernel iterations, automatic canary decisions and production-cluster deployment. Covers colocated and disaggregated backends; experiment resources scale with execution-group needs. Appendix A retains audited source references at fixed commits.
- `03_研究构想_MaaS集群PD配比弹性调整.md` — separate preliminary research direction: MaaS workload-driven P/D capacity ratios, reserve execution groups, preparation/activation/drain/reclamation, transition costs and capacity recovery. Role rotation belongs to this document.
- `papers.json` — manifest of record: per-paper id, venue, URLs, `file`, `status`, `bytes`, `sha256`, version notes. 33 entries. Ids 01–17, 21–27 and 33 have independently verified venue/program identities; 18–20 and 28–32 are author/preprint or unresolved-publication entries. TaiChi is a future SC 2026 program entry. TokenScale v2 labels itself SoCC 2026 but the official same-author program entry is titled TokenPipe; do not silently merge their titles. HFX v3 replaces the earlier title HyperFlexis. New arXiv versions are pinned after checking their history. Failed download attempts are printed to stderr by the downloader, not stored.
- `papers/` and `paper-text/` — downloaded PDFs and their PDFKit-extracted text (page-boundary-preserving, `NN_Name.pdf` ↔ `NN_Name.txt`).
- `references.bib` — one BibTeX entry per paper (count must equal `papers.json`).
- `evidence/` — append-only audit JSONs with timestamps, file SHA-256s, and scope notes. `source-audit-2026-11-03.json` is the current combined framework/PD audit of `/Users/zkx/vllm` and `/Users/zkx/sglang` at the user-provided local HEADs; earlier source and PD audits remain unchanged historical records. `framework-parameter-inventory-2026-11-03.json` counts selected current classes; the 2026-10-31 inventory retains its original broader scope; `web-verification.json` records primary-source verification of papers and, under `workload_traces`, the public LLM workload traces (Azure 2023/2024, BurstGPT, Mooncake) cited in the proposal; `self_evolving_serving_related_work` in the same file records the 2026 preprints, the GLM-5.3 model card, and TuxBot's LLM backend; `tuxbot-parameter-audit-*.json` pins the two TuxBot source files archived alongside it. `autopoiesis-close-reading-2026-11-05.json` pins local PDF/text evidence for the Part I §1.4 close reading, including the main-text/Appendix D model mismatch and Figure 7 ratio-versus-reduction mismatch. `herschel-close-reading-2026-11-05.json` pins the 17-page full-paper review, line-block hashes, figures/tables and the profiling/PD-experiment/external-rollout boundaries. `flashvector-close-reading-2026-11-05.json` records the full reread of the nine-page v1, isolated production replay, PR/canary, continuous triggering and Table 4 SLO inconsistency. `pd-elasticity-literature-2026-11-06.json` records 13 new PD papers plus shared references, pinned artifacts and mechanism locations. Its companion `pd-elasticity-sources-2026-11-06/` contains short primary-source identity excerpts; existing evidence remains unchanged. `validation.json` is a local validator report and is git-ignored.

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

# Validate all offline artifacts; writes the git-ignored evidence/validation.json. Exits non-zero on any error.
python3 scripts/validate_research.py
```

`validate_research.py` is the project's test suite. It checks, per paper, PDF header/EOF, that `bytes`/`sha256` match the manifest, parsed page count > 0, page-marker count matches, and text present; globally it checks that every relative Markdown link resolves and that the BibTeX entry count equals the paper count. **Run it only when the user explicitly requests it. For routine edits, inspect diffs and the affected content/links; do not rerun the full validator automatically.**

## Research directions

- Main plan in `02_研究方案_MaaS影子实验与持续自优化.md`: mirror selected production requests into an experiment environment; run fast parameter/policy tuning and slow code/kernel/build iterations; evaluate correctness, workload representativeness and service gains; freeze candidates for real canary traffic and staged production-cluster deployment.
- Fast/slow describe modification and execution cost; shadow/canary/deployment describe validation and publication stages. Both optimization types are tested in the experiment environment before production use. Runtime updates use safe engine boundaries; build changes use deployment adapters.
- Keep experiment resources as a sized pool, not a fixed single GPU/node or a rotating P/D role. A complete candidate must fit its model-parallel and backend dependencies. Track sampling, replay, warmup, experiment interruptions and resource competition.
- Herschel already covers production MaaS profiling, mechanism analysis and idle/revocable PD experiments with expert review and external rollout. FlashVector covers ongoing code/configuration optimization, isolated production replay and shadow canary. Research increments require joint-budget, evidence-quality and automatic-publication results.
- Record human interventions, automatic promotion/rejection, erroneous promotion and recovery costs. Optimizer APIs may come from the target service, an internal replica or an external endpoint; retain confidentiality and full capacity/cost comparisons.
- Separate PD direction in `03_研究构想_MaaS集群PD配比弹性调整.md`: change resource ratios under workload shifts using reserve execution groups and explicit preparation, admission, drain and reclamation. Splitwise/EPD/FluidPD already cover dynamic roles; DistServe has replanning and Mooncake switches roles for significant shifts. Compare reserve-first and in-place transitions, natural drain and request migration, plus Libra-style unified execution under the same total-resource budget. Evaluate target ratios jointly with transition paths, spare capacity recovery and cumulative SLO delivery.
- Implementations and GPU experiments remain future work. Audited framework capabilities and immutable evidence retain their recorded dates, commits and scope. Appendix A in the main proposal remains the source-reference index.

## Conventions that matter (evidence discipline)

This project's whole value is provenance rigor. Preserve it:

- **Never invent or alter a number, hash, date, or claim.** Figures come only from the cited artifact. Keep `papers.json` sha256/bytes consistent with the actual files — the download script sets them; don't hand-edit to make validation pass.
- **Separate publication identity from downloaded version.** A paper can be accepted at a venue while the local PDF is an author arXiv version with *different* experimental numbers (e.g. TuxBot). Bind any quoted number to the specific version; never splice numbers across versions.
- **Separate "native capability" from "proposed, unimplemented extension."** In `02_研究方案_MaaS影子实验与持续自优化.md` and the audits, framework parameters are labeled as exposing existing policy, needing a new state-update protocol, or being a new algorithm. Do not describe proposed research interfaces as if the frameworks already support them.
- **Source links are pinned to fixed commits.** vLLM/SGLang references use the commit SHAs recorded in `source-audit-2026-11-03.json`; keep `[V*]`/`[S*]` link targets on those commits unless deliberately re-auditing.
- **Verify before writing; omit what cannot be confirmed.** Every paper, dataset, link, number, or claim added to the documents is fetched from a primary source first and recorded in `evidence/`. Content that cannot be confirmed is left out entirely rather than included with caveats. Do not cite from memory.
- **Document style.** Fold edits into existing sections instead of adding new ones, and write plain declarative statements rather than defensive phrasing.
- When adding a paper: add to `papers.json`, download, extract text, add a `references.bib` entry, cite it in the survey and keep counts/links consistent. Run the full validator only on explicit user request.

## Git

- Remote: `origin` → `https://github.com/zksainx/runtime-inference-autotuning-research.git` (public), branch `main`.
- Identity and the `store` credential helper are set in the **repository-local** config only. Never modify `git config --global`. Credentials live in `~/.git-credentials`; never print, read back, or commit them.
- Run `python3 scripts/validate_research.py` only when explicitly requested by the user, including before commits. Routine changes use focused diff/content checks.

### Commit message convention

Commit messages are written in **English** and follow this format:

```
<type>(<scope>): <summary>

<body>

<trailers>
```

**Header** — required, at most 72 characters.

- `type` — one of:
  - `docs` — content changes to the survey, proposal, or CLAUDE.md
  - `papers` — adding, replacing, or re-extracting papers (`papers/`, `paper-text/`, `papers.json`, `references.bib`)
  - `evidence` — new or updated audit/verification records in `evidence/`
  - `scripts` — changes to tooling in `scripts/`
  - `fix` — corrections of wrong facts, numbers, links, or broken tooling
  - `chore` — repository maintenance (`.gitignore`, layout, config)
- `scope` — optional, the area touched: `survey` (`01_顶会论文调研.md`), `proposal` (`02_研究方案_MaaS影子实验与持续自优化.md`), `claude-md`, `manifest`, `bib`, `traces`, `source-audit`, `validator`, `extractor`, `downloader`. Omit the scope when a change spans several areas.
- `summary` — imperative mood ("add", "update", "remove", not "added"/"adds"), lowercase first word, no trailing period. Paper and framework names keep their own capitalization (vLLM, SGLang, TuxBot).

**Body** — required unless the header says everything. Separate from the header with one blank line and wrap at 72 characters. Explain what changed and why; for factual changes, name the source that supports it (paper section, URL, evidence file). Use `-` bullets for multiple points.

**Trailers** — separated from the body by one blank line. Commits produced with Claude Code end with:

```
Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
```

**Granularity** — one logical change per commit. A paper addition, for example, goes in a single `papers` commit containing the PDF, extracted text, and manifest and bib entries; the survey text that cites it goes in a separate `docs(survey)` commit.

**Examples**

```
docs(proposal): define two-layer framework modification scope

- Clarify that non-intrusiveness constrains client-visible behavior,
  not the amount of in-engine change.
- Describe the thin control plane with per-engine adapters and the
  in-engine changes required by class B mechanisms.

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
```

```
evidence(traces): record verification of public LLM workload traces

Fields and collection windows for the Azure 2023/2024, BurstGPT, and
Mooncake traces, confirmed from repository pages, the arXiv abstract,
and the first records of the Mooncake JSONL files.

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
```

```
fix(survey): bind TuxBot speedup figures to arXiv v2
```
