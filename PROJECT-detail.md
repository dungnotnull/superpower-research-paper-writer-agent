# PROJECT-detail.md — research-paper-writer

## Executive Summary

`research-paper-writer` is an autonomous harness skill that converts a user-provided research topic into a complete, citation-backed academic paper draft. The harness orchestrates seven sequential stages — literature discovery, gap analysis, outline planning, parallel section writing, cross-peer review, reference gathering, and quality validation — before assembling and delivering a structured `.md` paper file. It is designed for graduate students, independent researchers, and knowledge workers who need a rigorous, evidence-based first draft in minutes rather than weeks.

---

## Problem Statement

Academic writing requires three distinct capabilities that are rarely co-located in one person: (1) systematic literature search and synthesis, (2) critical gap identification, and (3) structured argumentation with proper citation. Most AI writing tools skip the first two and jump straight to generation, producing outputs that are confident but uncited, repetitive of existing work, and unaware of what questions remain open. This skill enforces the research-first principle: **no sentence is written until the supporting evidence has been located and assessed**.

---

## Target Users & Use Cases

| User | Trigger | Expected Output |
|------|---------|----------------|
| Graduate student | "Write a literature review on transformer attention mechanisms" | Full IMRaD paper with 15+ citations, gap analysis, proper APA references |
| Independent researcher | "I need a paper on climate change impact on coral reefs for a conference" | Conference-length paper (4,000–8,000 words) with abstract, sections, IEEE references |
| Knowledge worker | "Give me a research paper on the ROI of remote work policies" | Theme-based paper with business + academic sources, executive abstract |
| Educator | "Create a teaching paper on Bayesian statistics for undergraduates" | Pedagogically structured paper with introductory tone, worked examples cited |

---

## Harness Architecture

```
INPUT: User topic + citation style preference (APA/MLA/IEEE, default: APA)
  │
  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 1: Literature Discovery                                       │
│ sub-topic-researcher.md                                             │
│ • WebSearch ArXiv, Semantic Scholar, PubMed (date range ≤3 years)  │
│ • Collect ≥15 papers with title, authors, year, DOI, abstract      │
│ • Score each paper: recency × relevance × citation-count           │
│ • Output: annotated_bibliography.md                                 │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 2: Gap Analysis                                               │
│ sub-gap-analyzer.md + invoke research-first-reasoning              │
│ • Apply devil's advocate analysis to existing literature           │
│ • Identify 3–5 genuine knowledge gaps with evidence                │
│ • Prioritize gaps by impact and feasibility to address             │
│ • Output: gap_matrix.md                                            │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 3: Outline Planning                                           │
│ sub-outline-planner.md                                              │
│ • Select structure: IMRaD (empirical) or thematic (review/survey)  │
│ • Map each section → primary sources + gaps to address             │
│ • Assign word targets per section                                   │
│ • Output: paper_outline.md                                         │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 4: Parallel Section Writing                                   │
│ sub-section-writer.md [one agent instance per section]             │
│ • Each agent writes one section (Introduction / Related Work /     │
│   Methodology / Results / Discussion / Conclusion / Abstract)      │
│ • Every sentence grounded in ≥1 citation from bibliography         │
│ • Output: section_draft_{name}.md per section                      │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 5: Cross-Peer Review                                          │
│ sub-cross-reviewer.md                                               │
│ • Agent A reviews Agent B's section and vice versa                 │
│ • Check: coherence, citation accuracy, logical flow, tone          │
│ • Produce revision notes for each section                          │
│ • Section writer applies revisions                                  │
│ • Output: section_revised_{name}.md per section                    │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 6: Reference Gathering                                        │
│ sub-reference-gatherer.md                                           │
│ • Collect all DOIs/URLs cited across all sections                  │
│ • Resolve metadata via CrossRef API / Semantic Scholar API         │
│ • Format in selected citation style (APA/MLA/IEEE)                 │
│ • Run duplicate-detection (DOI hash) — flag duplicates             │
│ • Output: references.md                                            │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 7: Quality Validation (Gate)                                  │
│ sub-quality-validator.md                                            │
│ • Verify: every factual claim has ≥1 citation                      │
│ • Verify: evidence hierarchy respected                             │
│ • Verify: abstract accurately summarizes body                      │
│ • Verify: no duplicate citations in reference list                 │
│ • Verify: word count meets target (≥3,000 words)                   │
│ • GATE: if fails → return to Stage 4/5 for revision               │
│ • Output: validation_report.md                                     │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ASSEMBLY                                                            │
│ Concatenate all revised sections + references                      │
│ Write to output/paper-{topic-slug}.md                              │
│ Report file path to user                                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Full Sub-Skill Catalog

### sub-topic-researcher.md
- **Purpose:** Search and collect recent scientific literature on the user's topic
- **Inputs:** User topic string, optional date range (default: last 3 years), optional domain filter
- **Outputs:** `annotated_bibliography.md` — table of ≥15 papers with metadata + relevance score
- **Tools:** WebSearch, WebFetch
- **Quality Gate:** Must find ≥15 papers; ≥50% must have DOIs and be from peer-reviewed venues

### sub-gap-analyzer.md
- **Purpose:** Analyze the bibliography to identify genuine knowledge gaps
- **Inputs:** `annotated_bibliography.md`
- **Outputs:** `gap_matrix.md` — list of 3–5 gaps with supporting evidence and priority rank
- **Tools:** Read, Skill(research-first-reasoning)
- **Quality Gate:** Each gap must be supported by ≥2 papers confirming the absence/limitation

### sub-outline-planner.md
- **Purpose:** Design a structured paper outline mapped to sources
- **Inputs:** `gap_matrix.md`, `annotated_bibliography.md`, user's paper type preference
- **Outputs:** `paper_outline.md` — section list with word targets and assigned sources
- **Tools:** Read, Write
- **Quality Gate:** Outline must cover all identified gaps; every section maps to ≥2 sources

### sub-section-writer.md
- **Purpose:** Write a single paper section grounded in cited evidence
- **Inputs:** `paper_outline.md` (target section), `annotated_bibliography.md`
- **Outputs:** `section_draft_{name}.md` — drafted section with inline citations
- **Tools:** Read, Write, WebFetch (for full abstract access if needed)
- **Quality Gate:** Every factual claim must have an inline citation; no fabricated statistics

### sub-cross-reviewer.md
- **Purpose:** Peer-review a section drafted by another sub-agent instance
- **Inputs:** `section_draft_{name}.md`, `paper_outline.md`
- **Outputs:** `section_revised_{name}.md` with revision notes + accepted revisions applied
- **Tools:** Read, Write
- **Quality Gate:** Reviewer must flag ≥1 issue or explicitly certify "no revisions needed"

### sub-reference-gatherer.md
- **Purpose:** Collect all citations, resolve metadata, format in citation style
- **Inputs:** All `section_revised_*.md` files, user's citation style choice
- **Outputs:** `references.md` — formatted reference list + `duplicate_report.md`
- **Tools:** WebFetch (CrossRef, Semantic Scholar APIs), Write
- **Quality Gate:** Every in-text citation appears in reference list; no duplicate DOIs

### sub-quality-validator.md
- **Purpose:** Final validation gate before paper assembly
- **Inputs:** All `section_revised_*.md`, `references.md`, `gap_matrix.md`
- **Outputs:** `validation_report.md` — PASS/FAIL with itemized checklist
- **Tools:** Read, Write
- **Quality Gate:** All checklist items must PASS; FAIL returns to Stage 4

---

## Skill File Format Specification

Each skill file uses this frontmatter schema:

```yaml
---
name: <skill-name>
description: <one-line summary>
---
```

Required sections in every skill file:
- `## Role & Persona` — who Claude becomes
- `## Workflow (Harness Flow)` — numbered sequential steps
- `## Sub-skills Available` — list of invokable child skills
- `## Tools` — tools used
- `## Output Format` — exact deliverable structure
- `## Quality Gates` — checklist before output is shown

---

## E2E Execution Flow

```
1. User invokes: /research-paper-writer
2. Harness prompts: "Enter your research topic:" + "Citation style (APA/MLA/IEEE, default APA):"
3. Stage 1: invoke sub-topic-researcher → write annotated_bibliography.md
4. Gate: bibliography has ≥15 papers? → if No: expand search, adjust date range
5. Stage 2: invoke sub-gap-analyzer → write gap_matrix.md
6. Gate: 3–5 gaps identified with evidence? → if No: request broader literature search
7. Stage 3: invoke sub-outline-planner → write paper_outline.md
8. Gate: all gaps addressed in outline? → if No: revise outline
9. Stage 4: invoke sub-section-writer × N sections (parallel) → write section_draft_*.md files
10. Gate: all sections drafted with inline citations? → if No: retry failed sections
11. Stage 5: invoke sub-cross-reviewer × N sections → write section_revised_*.md files
12. Stage 6: invoke sub-reference-gatherer → write references.md + duplicate_report.md
13. Gate: duplicate citations found? → if Yes: resolve duplicates
14. Stage 7: invoke sub-quality-validator → write validation_report.md
15. Gate: validation PASS? → if No: return to Stage 4 for targeted revision
16. Assembly: concatenate sections + references → write output/paper-{slug}.md
17. Report: "Paper written to output/paper-{slug}.md ({word_count} words, {N} citations)"
```

---

## SECOND-KNOWLEDGE-BRAIN Integration

**Sources crawled:**
- ArXiv (cs.AI, cs.LG, stat.ML, q-bio, econ, physics.soc-ph)
- Semantic Scholar API (all domains)
- PubMed (life sciences, medicine)
- CrossRef (DOI resolution and citation metadata)

**Crawl config (knowledge_updater.py):**
- Frequency: weekly
- Search queries: domain-adaptive (derived from skill topic)
- Scoring: recency (30%) + relevance (50%) + citation count (20%)
- Append format: see SECOND-KNOWLEDGE-BRAIN.md → Self-Update Protocol
- Deduplication: DOI hash check before append

---

## Quality Gates Definition

| Gate ID | Stage | Condition | Action on Fail |
|---------|-------|-----------|----------------|
| G1 | After Stage 1 | ≥15 papers found, ≥50% with DOIs | Expand date range; retry search |
| G2 | After Stage 2 | 3–5 gaps with ≥2 supporting papers each | Broaden literature search |
| G3 | After Stage 3 | All gaps addressed in outline | Revise outline sections |
| G4 | After Stage 4 | All sections drafted, all claims cited | Retry uncompleted sections |
| G5 | After Stage 6 | No duplicate citations | Merge duplicate references |
| G6 | After Stage 7 | All validation items PASS | Return to Stage 4 for targeted fixes |

---

## Test Scenarios

See `tests/test-scenarios.md` for 5+ complete scenario tests.

---

## Key Design Decisions

1. **Research-first, write-second**: No section is started until `annotated_bibliography.md` is complete and `gap_matrix.md` is approved. This prevents hallucinated claims.
2. **IMRaD as default structure**: Most scientific papers use Introduction/Methods/Results/Discussion. The planner selects thematic structure only for review/survey papers.
3. **Citation style selection at intake**: Collecting the user's preference upfront avoids reformatting the entire reference list after writing.
4. **Parallel section writing**: Each section is written by a separate sub-agent invocation to maintain independent voice and prevent cross-contamination of arguments.
5. **Cross-review, not self-review**: A different agent instance reviews each section to catch errors the original writer would miss.
6. **Plagiarism check via DOI deduplication**: Ensures each source appears once in references; flags suspiciously similar abstracts from different DOIs.
7. **Quality gate loop**: Stage 7 can send the paper back to Stage 4 for targeted revision — not a full restart — to maintain efficiency.
8. **Graceful degradation**: If WebSearch fails, the harness falls back to SECOND-KNOWLEDGE-BRAIN.md internal paper entries and signals the limitation to the user.
