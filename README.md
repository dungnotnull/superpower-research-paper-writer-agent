# 🧠 Superpower Research Paper Writer Agent

> **Autonomous academic research harness** — evaluate ideas, search literature, identify gaps, plan structure, write sections, review, and deliver a complete academic paper draft.

[![License: CC-BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-8A2BE2)](https://claude.ai)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](requirements.txt)
[![Supervisor-Skills](https://img.shields.io/badge/Enhanced%20with-Supervisor--Skills-orange)](https://github.com/HKUSTDial/Supervisor-Skills)

---

## What It Does

Give it a research topic — get back a complete academic paper draft. The agent runs a **10+ stage autonomous pipeline** that:

1. **Evaluates your research idea** using a five-dimension framework (Higher, Faster, Stronger, Cheaper, Broader), fatal-flaws audit, lifecycle matching, and paradigm-shift probing
2. **Plans the paper structure** with a thinking template and self-consistency checks
3. **Discovers recent literature** (≥15 papers from ArXiv, Semantic Scholar, PubMed)
4. **Identifies genuine knowledge gaps** with supporting evidence
5. **Plans a structured outline** (IMRaD or thematic) with source mapping
6. **Drafts a structured Introduction** using the six-paragraph flowchart method
7. **Writes sections in parallel** (≥500 words each, ≥3 citations per section)
8. **Designs scientific figures** with paradigm recommendations and quality audits
9. **Cross-reviews for accuracy** with peer-review protocol
10. **Gathers and formats references** (APA/MLA/IEEE + DOI dedup)
11. **Validates quality** (evidence hierarchy, citation checks)
12. **Runs pre-submission review** (macro logic, writing, grammar, format, figures, banned-vocabulary scan)
13. **Assembles the final paper** as a .md file

---

## Pipeline (v2.0)

```
INPUT: "Write a paper on [TOPIC]" + citation style (APA/MLA/IEEE)
  │
  ├─ Step 0a ─ Idea Evaluation (NEW, optional)
  │     5D scoring, fatal-flaws audit, paradigm-shift probe
  │     Verdict: Strong Accept / Accept with Revisions / Reject and Pivot
  │
  ├─ Step 0b ─ Paper Structure Planning (NEW, optional)
  │     Thinking template, paper-type positioning, 4 consistency checks
  │
  ├─ Step 1  ─ Intake
  ├─ Step 2  ─ Literature Discovery     → ≥15 papers
  ├─ Step 3  ─ Gap Analysis             → 3–5 knowledge gaps
  ├─ Step 4  ─ Outline Planning          → IMRaD/thematic structure
  │
  ├─ Step 4b ─ Introduction Drafting (NEW, optional)
  │     Six-paragraph flowchart outline
  │
  ├─ Step 5  ─ Parallel Section Writing  → 7 sections
  │
  ├─ Step 5b ─ Figure Design (NEW, optional)
  │     Paradigm recommendation, layout, quality audit
  │
  ├─ Step 6  ─ Cross-Peer Review        → revision notes
  ├─ Step 7  ─ Reference Gathering       → formatted references
  ├─ Step 8  ─ Quality Validation        → 8-point checklist
  │
  ├─ Step 8b ─ Pre-Submission Review (NEW, optional)
  │     5-dimension review + banned-vocabulary scan
  │
  └─ Assembly → output/paper-{topic}.md
```

---

## What's New in v2.0

This version integrates research methodology from [**Supervisor-Skills**](https://github.com/HKUSTDial/Supervisor-Skills) by Yuyu Luo (HKUST-GZ), licensed under CC-BY-4.0. The integration adds six new skills and 42 reference files:

### New Skills

| Skill | Purpose | Stage |
|-------|---------|-------|
| sub-idea-evaluator | Pre-pipeline idea evaluation: 5D scoring, fatal-flaws, paradigm-shift probe | Step 0a |
| sub-paper-structure-planner | Logical skeleton: thinking template, paper-type positioning, consistency checks | Step 0b |
| sub-intro-drafter | Six-paragraph Introduction flowchart with contribution alignment | Step 4b |
| sub-figure-designer | Scientific figure design: paradigm, layout, tools, quality audit | Step 5b |
| sub-pre-submission-reviewer | 5D review: logic, writing, grammar, format, figures, banned-vocabulary scan | Step 8b |
| sub-vibe-research-workflow | AI-assisted research ethics: behavioural rules, tool selection | Meta |

### Reference Materials (42 files)

| Directory | Contents |
|-----------|----------|
| skills/references/idea-evaluator/ | Five-dimension scoring, fatal-flaws, lifecycle matching, paradigm-shift probes (10 files) |
| skills/references/intro-drafter/ | Flowchart, paper-types, contribution patterns, running example, worked examples (5 files) |
| skills/references/paper-structure/ | Thinking template, consistency checks, paper types, worked examples (4 files) |
| skills/references/pre-submission-reviewer/ | Logic and structure, grammar rules, forbidden patterns, LaTeX rules, section guides (5 files) |
| skills/references/figure-designer/ | Design rules, motivated example, solution overview, experimental results, tools (5 files) |
| skills/references/vibe-research/ | Behaviour guidelines, vibe coding, vibe figure, vibe writing, tool selection (5 files) |
| skills/references/benchmark-paper/ | Gap analysis, benchmark design, construction pipeline, experiments, paper structure, checklist (8 files) |

---

## Quality Gates

| Gate | Stage | Condition | Action |
|------|-------|-----------|--------|
| G0a | Before Step 1 | Idea evaluation verdict (optional) | Proceed / Revise / Pivot |
| G0b | Before Step 1 | Paper structure consistency (optional) | Address chain breaks |
| G1 | After Step 2 | ≥15 papers found | Expand date range or warn user |
| G2 | After Step 3 | ≥3 gaps with evidence | Broaden analysis |
| G3 | After Step 4 | All gaps in outline | Revise outline |
| G4 | After Step 5 | All sections drafted + cited | Retry failed sections |
| G5 | After Step 7 | No duplicate citations | Merge duplicates |
| G6 | After Step 8 | Validation PASS | Return to Step 5 (max 2 cycles) |
| G7 | After Step 8b | Pre-submission review (optional) | Address CRITICAL findings |

---

## Skill Architecture

### Original Pipeline Skills (v1.0)

| File | Role |
|------|------|
| [skills/main.md](skills/main.md) | Harness orchestrator — stages, quality gates, assembly |
| [skills/sub-topic-researcher.md](skills/sub-topic-researcher.md) | Literature discovery via WebSearch |
| [skills/sub-gap-analyzer.md](skills/sub-gap-analyzer.md) | Knowledge gap identification with devil's advocate filtering |
| [skills/sub-outline-planner.md](skills/sub-outline-planner.md) | IMRaD/thematic structure design + source assignment |
| [skills/sub-section-writer.md](skills/sub-section-writer.md) | Per-section drafting with inline citation enforcement |
| [skills/sub-cross-reviewer.md](skills/sub-cross-reviewer.md) | Peer-review protocol (4 error types, revision notes) |
| [skills/sub-reference-gatherer.md](skills/sub-reference-gatherer.md) | CrossRef/DOI resolution + APA/MLA/IEEE formatting |
| [skills/sub-quality-validator.md](skills/sub-quality-validator.md) | Final validation gate (8 checks, PASS/FAIL verdict) |

### Enhanced Skills (v2.0 — from Supervisor-Skills)

| File | Role |
|------|------|
| [skills/sub-idea-evaluator.md](skills/sub-idea-evaluator.md) | Pre-pipeline idea evaluation: 5D scoring, fatal-flaws, paradigm-shift probe |
| [skills/sub-paper-structure-planner.md](skills/sub-paper-structure-planner.md) | Logical skeleton: thinking template, paper-type positioning, self-consistency checks |
| [skills/sub-intro-drafter.md](skills/sub-intro-drafter.md) | Six-paragraph Introduction flowchart with contribution alignment |
| [skills/sub-figure-designer.md](skills/sub-figure-designer.md) | Scientific figure design: paradigm, layout, tools, quality audit |
| [skills/sub-pre-submission-reviewer.md](skills/sub-pre-submission-reviewer.md) | 5D pre-submission review: logic, writing, grammar, format, figures |
| [skills/sub-vibe-research-workflow.md](skills/sub-vibe-research-workflow.md) | AI-assisted research workflow: behavioural rules, tool selection, integrity gate |

---

## Python Tooling

### Knowledge Pipeline
- [	ools/knowledge_updater.py](tools/knowledge_updater.py) — crawls ArXiv, Semantic Scholar, and PubMed; scores papers by recency × relevance × citation-count; deduplicates by DOI hash

### Citation Verification (from academic-research-skills v3.11)
- 	ools/arxiv_client.py — ArXiv API client
- 	ools/crossref_client.py — CrossRef DOI resolution
- 	ools/semantic_scholar_client.py — Semantic Scholar paper search
- 	ools/openalex_client.py — OpenAlex API client
- 	ools/verification_cache.py — SQLite-backed cache (90-day TTL)
- 	ools/citation_verification_summary.py — per-citation status tracking
- 	ools/verify_passport.py — CLI verification gate
- 	ools/uncited_assertion_detector.py — uncited claim detection
- 	ools/temporal_integrity_audit.py — temporal verification audit
- 	ools/claim_audit_pipeline.py — claim alignment & drift audit

### Literature Corpus Adapters
- [	ools/adapters/folder_scan.py](tools/adapters/folder_scan.py) — import from PDF folder
- [	ools/adapters/zotero.py](tools/adapters/zotero.py) — import from Zotero Better BibTeX JSON
- [	ools/adapters/obsidian.py](tools/adapters/obsidian.py) — import from Obsidian vault

### JSON Schemas
23 JSON schemas in [shared/schemas/](shared/schemas/) for structured data validation.

---

## Quick Start

### Prerequisites
- [Claude Code](https://claude.ai/code) with Skills support
- Python 3.10+ for tooling
- pip install -r requirements.txt

### Running the Skill

1. Invoke in Claude Code:
   `
   research-paper-writer
   `
2. The harness will ask for your topic and citation style.
3. Optionally run idea evaluation first:
   `
   Evaluate my research idea: [your idea]
   `
4. Wait for the pipeline to complete — the final paper appears at output/paper-{topic-slug}.md.

### Knowledge Auto-Update

```
python tools/knowledge_updater.py --topic "your research topic" --days 90
```

---

## Project Structure

```
.
├── .claude/
│   └── settings.json                    # Cron schedule + tool config
├── skills/
│   ├── main.md                          # Harness orchestrator (v2.0)
│   ├── sub-idea-evaluator.md            # NEW: Idea evaluation (5D, fatal-flaws, paradigm-shift)
│   ├── sub-paper-structure-planner.md   # NEW: Paper structure (thinking template, consistency)
│   ├── sub-intro-drafter.md             # NEW: Introduction flowchart (6-paragraph)
│   ├── sub-figure-designer.md           # NEW: Figure design (paradigm, layout, audit)
│   ├── sub-pre-submission-reviewer.md   # NEW: Pre-submission review (5D, banned-vocabulary)
│   ├── sub-vibe-research-workflow.md    # NEW: AI research ethics (Vibe Coding/Figure/Writing)
│   ├── sub-topic-researcher.md
│   ├── sub-gap-analyzer.md
│   ├── sub-outline-planner.md
│   ├── sub-section-writer.md
│   ├── sub-cross-reviewer.md
│   ├── sub-reference-gatherer.md
│   ├── sub-quality-validator.md
│   └── references/                     # NEW: 42 reference files from Supervisor-Skills
│       ├── idea-evaluator/
│       ├── intro-drafter/
│       ├── paper-structure/
│       ├── pre-submission-reviewer/
│       ├── figure-designer/
│       ├── vibe-research/
│       └── benchmark-paper/
├── tools/
│   ├── knowledge_updater.py
│   ├── adapters/
│   └── ... (12 Python scripts)
├── shared/
│   └── schemas/                         # 23 JSON validation schemas
├── tests/
├── output/
├── logs/
├── CLAUDE.md                             # Skill identity & task tracking (v2.0)
├── PROJECT-detail.md                     # Full technical specification
├── SECOND-KNOWLEDGE-BRAIN.md            # Self-improving knowledge base
├── README.md                             # This file (v2.0)
├── requirements.txt
└── announce-rpw-loaded.sh
```

---

## Cross-Skill Integration

- sub-idea-evaluator runs **before** the pipeline. Verdict determines whether to proceed.
- sub-paper-structure-planner runs **before** literature discovery. Output informs outline planning.
- sub-intro-drafter runs **after** outline planning. Output consumed by sub-section-writer.
- sub-figure-designer runs **during** section writing or standalone.
- sub-pre-submission-reviewer runs **after** quality validation. Comprehensive replacement for simple checklist.
- sub-vibe-research-workflow is a **meta-guide** invoked at any stage.
- sub-gap-analyzer invokes Skill("research-first-reasoning") at Step 5 for evidence hierarchy (with built-in fallback).
- sub-quality-validator invokes Skill("research-first-reasoning") at Step 3 for citation tier (with built-in fallback).
- All integrations have built-in fallbacks — if a skill is unavailable, the pipeline proceeds.

---

## Licensing

This project is **dual-purpose**:
- The skill specification (.md files, architecture, workflows) is **open** for academic and personal use.
- The integrated tooling from [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) retains its original license (CC-BY-NC 4.0).
- Enhanced skills and reference materials from [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) are licensed under CC-BY-4.0.

---

## Attribution

Five-dimension framework, fatal-flaws audit, lifecycle matching, paradigm-shift probe, six-paragraph Introduction flowchart, thinking template, self-consistency checks, paper-type positioning, contribution patterns, running-example design, figure design paradigms, pre-submission review dimensions, banned-vocabulary list, Vibe Research workflow, and behavioural rules are adapted from [**Supervisor-Skills**](https://github.com/HKUSTDial/Supervisor-Skills) by Yuyu Luo (HKUST-GZ), licensed under CC-BY-4.0.

---

## Author

**dungnotnull** & **Claude** (Anthropic) — built with ❤️ for open academic research.
