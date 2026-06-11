# CLAUDE.md — research-paper-writer

## Skill Identity

- **Skill Name:** research-paper-writer
- **Tagline:** Autonomous academic research harness — from idea evaluation to publishable-quality paper
- **Current Version:** v2.0 — Enhanced with Supervisor-Skills methodology
- **Skill File:** skills/main.md

---

## Problem This Skill Solves

Academic writing is time-intensive, fragmented, and requires deep domain fluency to locate relevant literature, identify genuine knowledge gaps, and synthesize findings into a coherent narrative. This skill transforms a single user-supplied topic into a full research paper draft by running an autonomous multi-agent harness: it evaluates the research idea, searches recent literature, identifies what has NOT been answered, plans a structured outline, distributes section writing across parallel sub-agents, conducts cross-review between agents, drafts a structured Introduction using the six-paragraph flowchart method, validates claims against cited sources, gathers and formats references, runs a comprehensive five-dimension pre-submission review, and delivers a complete .md paper file. The user only needs to provide a topic and a citation style preference.

---

## What's New in v2.0

This version integrates methodology from [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) by Yuyu Luo (HKUST-GZ), licensed under CC-BY-4.0. Key additions:

### New Pre-Pipeline Skills
- **sub-idea-evaluator**: Evaluates research ideas before pipeline entry using a five-dimension framework (Higher, Faster, Stronger, Cheaper, Broader), fatal-flaws audit, lifecycle and capability matching, and paradigm-shift probing. Verdict: Strong Accept, Accept with Revisions, or Reject and Pivot.
- **sub-paper-structure-planner**: Structures the paper's full logical skeleton using a thinking-template table, positions the paper type (Technique / New Problem/Setting / Benchmark / Cross-domain), and runs four self-consistency checks on the logic chain.

### New Writing-Phase Skills
- **sub-intro-drafter**: Drafts six-paragraph Introduction outlines using the flowchart method (Background, Limitations, Goal, Challenges, Solution, Contributions). Enforces contribution-to-challenge alignment and running-example consistency.
- **sub-figure-designer**: Advises on scientific figure design for the three core figures (Motivated Example, Solution Overview, Experimental Results). Recommends paradigms, layouts, tools, and runs a quality-control audit.

### New Post-Pipeline Skills
- **sub-pre-submission-reviewer**: Comprehensive five-dimension pre-submission review (macro logic, writing details, English grammar, format, figure quality) with banned-vocabulary and em-dash scanning, section-by-section checks, and severity-tagged findings (CRITICAL / MAJOR / MINOR).

### Meta-Skills
- **sub-vibe-research-workflow**: Guides AI-assisted research across Vibe Coding, Vibe Figure, and Vibe Writing phases with six non-negotiable behavioural rules for academic integrity and tool selection.

### Reference Materials
- skills/references/idea-evaluator/: Five-dimension scoring, fatal-flaws, lifecycle matching, paradigm-shift references (10 files)
- skills/references/intro-drafter/: Flowchart, paper-types, contribution patterns, running example, worked examples (5 files)
- skills/references/paper-structure/: Thinking template, consistency checks, paper types, worked examples (4 files)
- skills/references/pre-submission-reviewer/: Logic and structure, grammar rules, forbidden patterns, LaTeX rules, section guides (5 files)
- skills/references/figure-designer/: Design rules, motivated example, solution overview, experimental results, tools (5 files)
- skills/references/vibe-research/: Behaviour guidelines, vibe coding, vibe figure, vibe writing, tool selection (5 files)
- skills/references/benchmark-paper/: Gap analysis, benchmark design, construction pipeline, experiments, paper structure, checklist (8 files)

---

## Harness Flow Summary (v2.0)

`
User: "Write a research paper on [TOPIC]"
  │
  ├─ Step 0a ─ sub-idea-evaluator.md (NEW, optional)
  │     Evaluate idea: 5-dimension score, fatal flaws, paradigm shift
  │     Verdict: Strong Accept / Accept with Revisions / Reject and Pivot
  │
  ├─ Step 0b ─ sub-paper-structure-planner.md (NEW, optional)
  │     Fill thinking template, position paper type, 4 consistency checks
  │
  ├─ Step 1  ─ Intake (topic + citation style)
  │
  ├─ Step 2  ─ Literature Discovery     → ≥15 papers from ArXiv, Semantic Scholar, PubMed
  ├─ Step 3  ─ Gap Analysis             → 3–5 knowledge gaps with supporting evidence
  ├─ Step 4  ─ Outline Planning         → IMRaD or Thematic structure with source mapping
  │
  ├─ Step 4b ─ sub-intro-drafter.md (NEW, optional)
  │     Six-paragraph Introduction flowchart outline
  │
  ├─ Step 5  ─ Parallel Section Writing → 7 sections written simultaneously
  │
  ├─ Step 5b ─ sub-figure-designer.md (NEW, optional)
  │     Figure paradigm, layout, labelling, tool, quality audit
  │
  ├─ Step 6  ─ Cross-Peer Review        → Sections reviewed by peers
  ├─ Step 7  ─ Reference Gathering       → APA/MLA/IEEE formatting + DOI dedup
  ├─ Step 8  ─ Quality Validation        → 8-point checklist, evidence hierarchy
  │
  ├─ Step 8b ─ sub-pre-submission-reviewer.md (NEW, optional)
  │     5-dimension review + banned-vocabulary scan + grammar check
  │
  └─ Assembly → output/paper-{topic}.md
`

---

## Sub-Skills List

### Original Pipeline Skills (v1.0)
| File | Purpose |
|------|---------|
| skills/sub-topic-researcher.md | Literature discovery via WebSearch |
| skills/sub-gap-analyzer.md | Knowledge gap identification with devil's advocate filtering |
| skills/sub-outline-planner.md | IMRaD/thematic structure design + source assignment |
| skills/sub-section-writer.md | Per-section drafting with inline citation enforcement |
| skills/sub-cross-reviewer.md | Peer-review protocol (4 error types, revision notes) |
| skills/sub-reference-gatherer.md | CrossRef/DOI resolution + APA/MLA/IEEE formatting |
| skills/sub-quality-validator.md | Final validation gate (8 checks, PASS/FAIL verdict) |

### Enhanced Skills (v2.0 — from Supervisor-Skills)
| File | Purpose |
|------|---------|
| skills/sub-idea-evaluator.md | Pre-pipeline idea evaluation: 5D scoring, fatal-flaws, paradigm-shift probe |
| skills/sub-paper-structure-planner.md | Logical skeleton: thinking template, paper-type positioning, self-consistency checks |
| skills/sub-intro-drafter.md | Six-paragraph Introduction flowchart with running-example and contribution alignment |
| skills/sub-figure-designer.md | Scientific figure design: paradigm recommendation, layout sketch, quality audit |
| skills/sub-pre-submission-reviewer.md | Five-dimension pre-submission review: logic, writing, grammar, format, figures |
| skills/sub-vibe-research-workflow.md | AI-assisted research workflow: behavioural rules, tool selection, integrity gate |

---

## Tools Required

- WebSearch — search ArXiv, Semantic Scholar, PubMed, Google Scholar
- WebFetch — fetch paper abstracts, DOI metadata, citation data
- Read — read intermediate files between stages
- Write — write section drafts and final paper .md file
- Bash — run knowledge_updater.py for SECOND-KNOWLEDGE-BRAIN updates
- Skill — invoke esearch-first-reasoning for evidence-enforcement

---

## Integration Notes

- sub-idea-evaluator runs **before** the pipeline. If verdict is Reject and Pivot, the pipeline does not start.
- sub-paper-structure-planner runs **after** idea evaluation and **before** literature discovery. Its output informs outline planning and Introduction drafting.
- sub-intro-drafter runs **after** outline planning and **before** section writing. Its output is consumed by sub-section-writer for the Introduction.
- sub-figure-designer runs **during** section writing or as a standalone.
- sub-pre-submission-reviewer runs **after** quality validation and **before** assembly. It is a more comprehensive replacement for the simple 8-point checklist.
- sub-vibe-research-workflow is a **meta-guide** that can be invoked at any stage.
- All new skills have built-in fallbacks — if a skill is not available, the pipeline proceeds without it.

---

## Active Development Tasks

- [x] All v1.0 phases complete
- [x] Integrate Supervisor-Skills methodology into 6 new sub-skills
- [x] Copy reference materials (42 files across 7 directories)
- [x] Update main.md orchestrator with Steps 0a, 0b, 4b, 5b, 8b
- [x] Update CLAUDE.md with v2.0 changes
- [ ] Update README.md with v2.0 changes
- [ ] Commit and push to main

---

## Attribution

Five-dimension framework, fatal-flaws audit, lifecycle matching, paradigm-shift probe, six-paragraph Introduction flowchart, thinking template, self-consistency checks, paper-type positioning, contribution patterns, running-example design, figure design paradigms, pre-submission review dimensions, banned-vocabulary list, Vibe Research workflow, and behavioural rules are adapted from [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) by Yuyu Luo (HKUST-GZ), licensed under CC-BY-4.0.
