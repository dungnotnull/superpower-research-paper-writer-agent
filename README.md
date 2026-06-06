# 🧠 Superpower Research Paper Writer Agent

> **Autonomous academic research harness** — turn any topic into a rigorous, citation-backed paper draft in minutes.

[![License: CC-BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-8A2BE2)](https://claude.ai)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](requirements.txt)

---

## What It Does

Give it a research topic — get back a complete academic paper draft. The agent runs a **7-stage autonomous pipeline** that discovers recent literature, identifies genuine knowledge gaps, plans a structured outline, writes sections in parallel, cross-reviews for accuracy, gathers and formats references, and validates quality — all before assembling the final `.md` file.

This isn't a text generator. It's a **research engine** that won't write a single sentence until the evidence base is fully assembled and validated.

---

## Pipeline

```
INPUT: "Write a paper on [TOPIC]" + citation style (APA/MLA/IEEE)
  │
  ├─ Stage 1  —  Literature Discovery     →  ≥15 papers from ArXiv, Semantic Scholar, PubMed
  ├─ Stage 2  —  Gap Analysis             →  3–5 knowledge gaps with supporting evidence
  ├─ Stage 3  —  Outline Planning         →  IMRaD or Thematic structure with source mapping
  ├─ Stage 4  —  Parallel Section Writing →  7 sections written simultaneously (≥500 words each)
  ├─ Stage 5  —  Cross-Peer Review        →  Sections reviewed by peers, revision notes applied
  ├─ Stage 6  —  Reference Gathering      →  APA/MLA/IEEE formatting + DOI dedup
  ├─ Stage 7  —  Quality Validation       →  8-point checklist, evidence hierarchy enforcement
  │
  └─ Assembly  →  output/paper-{topic}.md
```

### Quality Gates

| Gate | Stage | Condition | Action |
|------|-------|-----------|--------|
| G1 | Literature | ≥15 papers found | Expand date range or warn user |
| G2 | Gap Analysis | ≥3 gaps with evidence | Broaden analysis |
| G3 | Outline | All gaps mapped to sections | Revise outline |
| G4 | Section Writing | ≥300 words, ≥3 citations per section | Retry failed sections |
| G5 | References | No duplicate DOIs | Merge duplicates |
| G6 | Validation | All 8 checklist items PASS | Return to Stage 4 (max 2 cycles) |

---

## Skill Architecture

The system is composed of **8 skill files** orchestrated by `skills/main.md`:

| File | Role |
|------|------|
| [`skills/main.md`](skills/main.md) | Harness orchestrator — stages, quality gates, assembly |
| [`skills/sub-topic-researcher.md`](skills/sub-topic-researcher.md) | Literature discovery via WebSearch |
| [`skills/sub-gap-analyzer.md`](skills/sub-gap-analyzer.md) | Knowledge gap identification with devil's advocate filtering |
| [`skills/sub-outline-planner.md`](skills/sub-outline-planner.md) | IMRaD/thematic structure design + source assignment |
| [`skills/sub-section-writer.md`](skills/sub-section-writer.md) | Per-section drafting with inline citation enforcement |
| [`skills/sub-cross-reviewer.md`](skills/sub-cross-reviewer.md) | Peer-review protocol (4 error types, revision notes) |
| [`skills/sub-reference-gatherer.md`](skills/sub-reference-gatherer.md) | CrossRef/DOI resolution + APA/MLA/IEEE formatting |
| [`skills/sub-quality-validator.md`](skills/sub-quality-validator.md) | Final validation gate (8 checks, PASS/FAIL verdict) |

Each sub-skill is a standalone Claude Skill file with its own role, workflow, tools, output format, and quality gates. They communicate through intermediate files in `1/output/`.

---

## Python Tooling

Built-in Python tools support the skill's research and verification pipeline:

### Knowledge Pipeline
- [`tools/knowledge_updater.py`](tools/knowledge_updater.py) — crawls ArXiv, Semantic Scholar, and PubMed; scores papers by recency × relevance × citation-count; deduplicates by DOI hash; appends new entries to `SECOND-KNOWLEDGE-BRAIN.md`. Scheduled via cron (`.claude/settings.json`).

### Citation Verification (integrated from [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) v3.11)
- `tools/arxiv_client.py` — ArXiv API client
- `tools/crossref_client.py` — CrossRef DOI resolution
- `tools/semantic_scholar_client.py` — Semantic Scholar paper search
- `tools/openalex_client.py` — OpenAlex API client
- `tools/verification_cache.py` — SQLite-backed cache (90-day TTL)
- `tools/citation_verification_summary.py` — per-citation status tracking
- `tools/verify_passport.py` — CLI verification gate
- `tools/uncited_assertion_detector.py` — uncited claim detection
- `tools/temporal_integrity_audit.py` — temporal verification audit
- `tools/claim_audit_pipeline.py` — claim alignment & drift audit

### Literature Corpus Adapters
- [`tools/adapters/folder_scan.py`](tools/adapters/folder_scan.py) — import from PDF folder
- [`tools/adapters/zotero.py`](tools/adapters/zotero.py) — import from Zotero Better BibTeX JSON
- [`tools/adapters/obsidian.py`](tools/adapters/obsidian.py) — import from Obsidian vault
- [`tools/adapters/_common.py`](tools/adapters/_common.py) — shared helpers

### JSON Schemas
23 JSON schemas in [`shared/schemas/`](shared/schemas/) for structured data validation (passport contracts, audit contracts, evaluation contracts).

---

## Test Scenarios

All **7 test scenarios** pass:

| # | Scenario | Status |
|---|----------|--------|
| 1 | Standard academic topic (transformer attention) | ✅ PASS |
| 2 | Interdisciplinary topic (ML × mental health) | ✅ PASS |
| 3 | Niche/sparse literature topic (quantum RNA folding) | ✅ PASS |
| 4 | Citation style selection (IEEE) | ✅ PASS |
| 5 | Edge case: quality gate rejection loop (empty topic) | ✅ PASS |
| 6 | WebSearch failure fallback → SECOND-KNOWLEDGE-BRAIN | ✅ PASS |
| 7 | research-first-reasoning meta-skill integration | ✅ PASS |

Run them yourself:
```bash
python tests/run_test_scenario.py --all
```

---

## Cross-Skill Integration

This skill integrates with the **`research-first-reasoning`** meta-skill (Skill 7) at two points:

1. **Gap Analysis** — validates each proposed gap against the evidence hierarchy (cohort-level evidence minimum)
2. **Quality Validation** — verifies every major claim's citation tier

Both integrations include **built-in fallbacks** — if Skill 7 is not installed, the harness automatically self-validates using its own evidence hierarchy logic. No circular dependency exists between the skills.

---

## Quick Start

### Prerequisites
- [Claude Code](https://claude.ai/code) with Skills support
- Python 3.10+ for tooling
- `pip install -r requirements.txt`

### Running the Skill

1. Invoke in Claude Code:
   ```
   research-paper-writer
   ```
2. The harness will ask for your topic and citation style.
3. Wait for the pipeline to complete — the final paper appears at `output/paper-{topic-slug}.md`.

### Knowledge Auto-Update

The knowledge base refreshes automatically every Monday at 09:00:
```bash
# Or run manually:
python tools/knowledge_updater.py --topic "your research topic" --days 90
```

---

## Project Structure

```
.
├── .claude/
│   └── settings.json           # Cron schedule + tool config
├── skills/
│   ├── main.md                 # Harness orchestrator
│   ├── sub-topic-researcher.md
│   ├── sub-gap-analyzer.md
│   ├── sub-outline-planner.md
│   ├── sub-section-writer.md
│   ├── sub-cross-reviewer.md
│   ├── sub-reference-gatherer.md
│   └── sub-quality-validator.md
├── tools/
│   ├── knowledge_updater.py    # Knowledge base crawler
│   ├── adapters/               # Literature corpus importers
│   └── ... (12 Python scripts) # Citation verification toolkit
├── shared/
│   └── schemas/                # 23 JSON validation schemas
├── tests/
│   ├── test-scenarios.md       # 7 scenario specifications
│   ├── run_test_scenario.py    # Automated test runner
│   └── test_results.md         # Execution results (7/7 PASS)
├── CLAUDE.md                   # Skill identity & task tracking
├── PROJECT-detail.md           # Full technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md
├── SECOND-KNOWLEDGE-BRAIN.md   # Self-improving knowledge base
├── requirements.txt            # Python dependencies
└── announce-rpw-loaded.sh      # SessionStart hook
```

---

## Architecture & Design

Detailed design documents:

- [`CLAUDE.md`](CLAUDE.md) — skill identity, harness flow, sub-skill table, active dev tasks
- [`PROJECT-detail.md`](PROJECT-detail.md) — full technical specification, architecture, design decisions
- [`SECOND-KNOWLEDGE-BRAIN.md`](SECOND-KNOWLEDGE-BRAIN.md) — domain knowledge base with evidence hierarchy, citation styles, gap analysis methodology, and research papers table
- [`PROJECT-DEVELOPMENT-PHASE-TRACKING.md`](PROJECT-DEVELOPMENT-PHASE-TRACKING.md) — build roadmap across 7 phases (all complete)

---

## Licensing

This project is **dual-purpose**:
- The skill specification (`.md` files, architecture, workflows) is **open** for academic and personal use.
- The integrated tooling from [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) retains its original license (CC-BY-NC 4.0).

---

## Author

**dungnotnull** & **Claude** (Anthropic) — built with ❤️ for open academic research.
