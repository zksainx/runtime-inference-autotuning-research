# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **research repository** (not a software product): a verified literature survey plus four research designs on *runtime autotuning of production LLM inference frameworks* (vLLM V1 and SGLang). There is no application to build. The deliverables are prose documents backed by downloaded papers and audit artifacts. No framework code has been modified and no GPU experiments have been run yet.

The survey and four research designs are written in **Chinese**; match that language when editing them. The `scripts/` tooling and `evidence/*.json` are in English.

## Layout

- `01_顶会论文调研.md` — literature survey: six major parts corresponding to shadow optimization (Part I), PD elasticity (Part II), parameterized scheduling (Part III), fixed-layout PD routing/admission (Part IV), EP/KV RDMA coordination (Part V), and soft-boundary PD/cache scheduling (Part VI). Part I retains 17 verified venue papers, the detailed Herschel/Autopoiesis/FlashVector v1 readings in §1.4 and related preprints in §1.7. Part II adds 13 papers (ids 21–33). Part III adds 6 verified conference papers (34–39): PIFO, Universal Packet Scheduling, Eiffel, Decima, VTC and Tail-Aware Scheduling. Part IV adds 12 papers (40–51): MAPS (ICML 2026), QUARTZ (Findings of ACL 2026), PPD (ICML 2026; archived arXiv v1), Strata (OSDI 2026), and eight other pinned preprints (including TetriInfer author v1). Part V adds 8 papers (52–59): Lina (USENIX ATC 2023), CASSINI (NSDI 2024) and six pinned author/preprint artifacts, with DualPath (SIGCOMM 2026; archived arXiv v2) as the direct KV-vs-EP isolation baseline. Part VI adds AMPD (ICML 2026, id 60), Vesta (61), Bursts (62), Remote KV Tiers (63) and KVCompass (POMACS 2026, id 64), and reuses the PD/cache literature. Across the six parts, 40 venue/program identities are independently confirmed (including one Findings paper and TaiChi in the future SC 2026 program on 2026-11-18); 24 author/preprint or unresolved-publication entries are separate. §2.7–2.8 contain shared artifacts. Each reference separates publication identity from the downloaded version.
- `02_研究方案_MaaS影子实验与持续自优化.md` — main research proposal: production observation, shadow-traffic experiments, fast configuration/policy tuning and slow code/kernel iterations, automatic canary decisions and production-cluster deployment. Covers colocated and disaggregated backends; experiment resources scale with execution-group needs. Appendix A retains audited source references at fixed commits.
- `03_研究构想_MaaS集群PD配比弹性调整.md` — separate preliminary research direction: MaaS workload-driven P/D capacity ratios, reserve execution groups, preparation/activation/drain/reclamation, transition costs and capacity recovery. Role rotation belongs to this document.
- `04_研究方案_参数化调度器的表达能力与在线优化.md` — third direction: fixed scheduling primitives, explicit persistent state, bounded parameters, constructive coverage and counterexamples, conditional safety/progress proof drafts, versioned updates and online adaptation. Kernel profiles are a secondary extension; no implementation or machine-checked proof is claimed.
- `05_研究方案_PD分离下的SLO感知在途工作量控制.md` — fixed-layout SLO-aware work-in-progress control: release prefill based on near-term downstream capacity and actual KV lifecycle; measure retained KV, blocked admissions, recompute, starvation and net SLO delivery. Holds routing and local scheduler fixed in primary comparisons. One selected research question; implementation and PD evaluation are planned.
- `06_研究方案_PD分离下EP通信与KV传输的RDMA协同.md` — MLA MoE PD disaggregation with cross-node EP on P and D over RoCE on the AMD ROCm stack: measure how DSCP/TC priority isolation protects EP all-to-all against KV transfer, then coordinate the low-priority class's residual capacity with prefill release, KV handoff and TTFT. DualPath already covers interference identification, static VL/TC isolation and DRAM buffering. Implementation and experiments are planned.
- `07_研究方案_软边界PD与三级缓存全局调度.md` — asymmetric soft-boundary PD under a fixed GPU budget: jointly schedule recompute or cache recovery, holder/tier/source state, four L3 load/compute paths and D-side append budgets. Account for HBM/DRAM byte-seconds, queueing externalities and a common closed-loop stability budget. Sustained-load evaluation measures warm-prefill offload and indirect P-queue relief; full physical role conversion belongs to proposal 03.
- `papers.json` — manifest of record: per-paper id, venue, URLs, `file`, `status`, `bytes`, `sha256`, version notes. 64 entries. Ids 01–17, 21–27, 33–39, 45–46, 49–50, 52–53, 57, 60 and 64 have verified venue/program identities; 46 is Findings of ACL, not ACL main. Ids 18–20, 28–32, 40–44, 47–48, 51, 54–56, 58–59 and 61–63 are author/preprint or unresolved-publication entries. TaiChi is a future SC 2026 program entry. TokenScale v2 labels itself SoCC 2026 but the official same-author program entry is titled TokenPipe; do not silently merge their titles. HFX v3 replaces the earlier title HyperFlexis. MLCC (arXiv 2402.09589 v2) extends MLTCP (HotNets 2024); keep the titles separate. New arXiv versions are pinned after checking their history. Failed download attempts are printed to stderr by the downloader, not stored.
- `papers/` and `paper-text/` — downloaded PDFs and their PDFKit-extracted text (page-boundary-preserving, `NN_Name.pdf` ↔ `NN_Name.txt`).
- `references.bib` — one BibTeX entry per paper (count must equal `papers.json`).
- `evidence/` — append-only audit JSONs with timestamps, file SHA-256s, and scope notes. `source-audit-2026-11-03.json` is the current combined framework/PD audit of `/Users/zkx/vllm` and `/Users/zkx/sglang` at the user-provided local HEADs; earlier source and PD audits remain unchanged historical records. `framework-parameter-inventory-2026-11-03.json` counts selected current classes; the 2026-10-31 inventory retains its original broader scope; `web-verification.json` records primary-source verification of papers and, under `workload_traces`, the public LLM workload traces (Azure 2023/2024, BurstGPT, Mooncake) cited in the proposal; `self_evolving_serving_related_work` in the same file records the 2026 preprints, the GLM-5.3 model card, and TuxBot's LLM backend; `tuxbot-parameter-audit-*.json` pins the two TuxBot source files archived alongside it. `autopoiesis-close-reading-2026-11-05.json` pins local PDF/text evidence for the Part I §1.4 close reading, including the main-text/Appendix D model mismatch and Figure 7 ratio-versus-reduction mismatch. `herschel-close-reading-2026-11-05.json` pins the 17-page full-paper review, line-block hashes, figures/tables and the profiling/PD-experiment/external-rollout boundaries. `flashvector-close-reading-2026-11-05.json` records the full reread of the nine-page v1, isolated production replay, PR/canary, continuous triggering and Table 4 SLO inconsistency. `pd-elasticity-literature-2026-11-06.json` records 13 new PD papers plus shared references, pinned artifacts and mechanism locations. Its companion `pd-elasticity-sources-2026-11-06/` contains short primary-source identity excerpts; existing evidence remains unchanged. `ep-kv-rdma-coscheduling-2026-11-17.json` records the initial proposal-06 literature search and a focused AMD ROCm path audit at local HEADs SGLang `074aeaf6` and vLLM `60bd6dd2`, a scope distinct from the NVIDIA-path audits; `ep-kv-rdma-fulltext-review-2026-11-17.json` records the full-text reread of papers 52–59 and corrects the initial abstract-level DualPath reading. `soft-pd-cache-scheduling-2026-11-17.json` records the proposal-07 mechanism synthesis, artifact hashes, asymmetric scope and the official AMPD ICML 2026 archival. `soft-pd-cache-scheduling-review-2026-11-17.json` records the added Vesta/Bursts/Remote-KV/KVCompass sources, PPD/DualPath publication updates and the revised R/A/B/C/D resource and stability model. `validation.json` is a local validator report and is git-ignored.

## Commands

The new `evidence/parameterized-scheduler-research-2026-11-13.json` records primary sources and focused mechanism readings for papers 34–39, plus a separate audit of `/Users/kxzhang/vllm` at `3897f95cf17619137536d2a7d325d9c2f39dc38f` and `/Users/kxzhang/sglang` at `4b83f215f498bc0371587bfae4a9470f24e77737`. These differ from the historical `/Users/zkx/` November 3 audit; preserve both scopes. Read fixed blobs for new observations and do not label local HEADs as latest upstream.

`evidence/pd-slo-routing-research-2026-11-15.json` pins the focused Splitwise/Mooncake/Arrow/Libra/TaiChi/FluidPD/Tail-Aware/Llumnix rereads used by proposal 05 and references the fixed AgentX provenance audit in the separate local implementation project. It does not establish novelty, framework support or PD performance. `evidence/pd-routing-literature-2026-11-15.json` records the subsequent 11-paper supplement, source/version boundaries, excluded identity mismatch, and the historical three-candidate discussion. `evidence/pd-wip-focus-2026-11-15.json` records the subsequent selection of one WIP-control question, TetriInfer v1, and pinned SGLang source evidence.

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
- Third direction in `04_研究方案_参数化调度器的表达能力与在线优化.md`: define a useful bounded policy class before claiming coverage; match whole event/decision traces, not only ranking. Keep executor invariants and persistent service accounting across parameter epochs. Evaluate representation, hot-path overhead, search cost and cumulative service gains separately. Start with vLLM single-instance dense text; SGLang/TP and a few compatible prefill kernel profiles follow. Do not equate decode with untunable or prefill with graph-free.
- PD work-in-progress direction in `05_研究方案_PD分离下的SLO感知在途工作量控制.md`: fix model, total resources, P/D roles, routing and local scheduler; control prefill release using downstream near-term capacity and real allocation/transfer/release events. Compare tuned fixed request/byte budgets, native admission, P-start binding, and MAPS/TetriInfer-style decode reservation. Source-side retained KV, blocked work, recompute and starvation must explain net SLO benefit beyond relocating waiting. Receiver interference and forecast uncertainty are evaluation factors within this one question.
- EP/KV RDMA direction in `06_研究方案_PD分离下EP通信与KV传输的RDMA协同.md`: treat DualPath-style static priority isolation as the baseline; measure residual coupling on AMD RoCE lossless TCs, then evaluate residual-capacity-aware prefill release and KV/prefetch submission at scheduler time scales. Sub-millisecond software interleaving is a feasibility comparator only. mori EP and Mooncake transport details still need a dedicated source audit.
- Soft-boundary PD direction in `07_研究方案_软边界PD与三级缓存全局调度.md`: treat DualPath loading, PPD/AMPD local prefill, Splitwise mixed pooling and FluidPD role switching as existing mechanisms. Evaluate R/A/B/C/D with holder/tier state, HBM/DRAM byte-seconds, queueing externalities and a common closed-loop session working-set budget. Sustained P-load experiments measure warm-prefill offload and indirect P-queue relief; proposal 03 owns full physical role conversion.
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
