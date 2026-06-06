# CLAUDE.md — research-paper-writer

## Skill Identity

- **Skill Name:** research-paper-writer
- **Tagline:** Autonomous academic research harness — from topic to published-quality paper
- **Current Phase:** Phase 0 — Architecture Complete, Ready for Phase 1
- **Skill File:** `skills/main.md`

---

## Problem This Skill Solves

Academic writing is time-intensive, fragmented, and requires deep domain fluency to locate relevant literature, identify genuine knowledge gaps, and synthesize findings into a coherent narrative. This skill transforms a single user-supplied topic into a full research paper draft by running an autonomous multi-agent harness: it searches recent literature, identifies what has NOT been answered, plans a structured outline, distributes section writing across parallel sub-agents, conducts cross-review between agents, validates claims against cited sources, gathers and formats references, and delivers a complete `.md` paper file. The user only needs to provide a topic and a citation style preference.

---

## Harness Flow Summary

```
User: "Write a research paper on [TOPIC]"
  │
  ├─ Stage 1 ─ sub-topic-researcher.md
  │     Search ArXiv, Semantic Scholar, PubMed for papers published ≤3 years
  │     Output: annotated bibliography (≥15 papers)
  │
  ├─ Stage 2 ─ sub-gap-analyzer.md
  │     Apply research-first-reasoning meta-skill
  │     Identify 3–5 genuine knowledge gaps / unanswered questions
  │     Output: gap matrix with evidence
  │
  ├─ Stage 3 ─ sub-outline-planner.md
  │     Design structured paper outline (IMRaD or theme-based)
  │     Map each section to relevant papers + gap evidence
  │     Output: section plan with assigned sources
  │
  ├─ Stage 4 ─ sub-section-writer.md  [runs per section in parallel]
  │     Write each section as a separate sub-agent task
  │     Each section grounded in cited sources only
  │     Output: drafted sections (Introduction, Methods, Results, Discussion, Conclusion)
  │
  ├─ Stage 5 ─ sub-cross-reviewer.md
  │     Each sub-agent reviews a peer's section for accuracy & coherence
  │     Produce revision notes
  │     Output: revision-annotated sections
  │
  ├─ Stage 6 ─ sub-reference-gatherer.md
  │     Collect all cited DOIs/URLs, resolve metadata (authors, year, venue)
  │     Format in user-selected citation style (APA/MLA/IEEE)
  │     Run plagiarism/duplicate-detection check
  │     Output: formatted reference list + duplicate-detection report
  │
  ├─ Stage 7 ─ sub-quality-validator.md
  │     Enforce evidence hierarchy (SR > MA > RCT > Cohort > Expert)
  │     Check every claim has a citation
  │     Validate abstract matches paper body
  │     Quality gate: must pass before assembly
  │
  └─ Assembly → writes final paper to `output/paper-{topic-slug}.md`
        Reports file path to user
```

---

## Sub-Skills List

| File                               | Purpose                                                 |
| ---------------------------------- | ------------------------------------------------------- |
| `skills/sub-topic-researcher.md`   | Search recent literature; return annotated bibliography |
| `skills/sub-gap-analyzer.md`       | Analyze papers; identify genuine knowledge gaps         |
| `skills/sub-outline-planner.md`    | Design IMRaD or theme-based paper outline               |
| `skills/sub-section-writer.md`     | Write individual paper sections, grounded in citations  |
| `skills/sub-cross-reviewer.md`     | Peer-review sections between sub-agents                 |
| `skills/sub-reference-gatherer.md` | Collect, format, and deduplicate all references         |
| `skills/sub-quality-validator.md`  | Final quality gate before paper assembly                |

---

## Tools Required

- `WebSearch` — search ArXiv, Semantic Scholar, PubMed, Google Scholar
- `WebFetch` — fetch paper abstracts, DOI metadata, citation data
- `Read` — read intermediate files between stages
- `Write` — write section drafts and final paper `.md` file
- `Bash` — run `knowledge_updater.py` for SECOND-KNOWLEDGE-BRAIN updates
- `Skill` — invoke `research-first-reasoning` for evidence-enforcement

---

## Knowledge Sources

| Source           | ArXiv Categories                   | Domain URLs                                           |
| ---------------- | ---------------------------------- | ----------------------------------------------------- |
| ArXiv            | cs.AI, cs.LG, stat.ML, q-bio, econ | https://arxiv.org/search/                             |
| Semantic Scholar | All domains                        | https://api.semanticscholar.org/graph/v1/paper/search |
| PubMed           | Life sciences, medicine            | https://pubmed.ncbi.nlm.nih.gov/                      |
| CrossRef         | DOI resolution                     | https://api.crossref.org/works                        |
| Unpaywall        | Open-access PDFs                   | https://unpaywall.org/data-format                     |

---

## Supporting Python Tools

- `tools/knowledge_updater.py` — crawl4ai pipeline that fetches latest papers from ArXiv, Semantic Scholar, PubMed; appends scored entries to `SECOND-KNOWLEDGE-BRAIN.md`
- `tools/arxiv_client.py` — dedicated ArXiv API client (from academic-research-skills v3.11)
- `tools/crossref_client.py` — CrossRef DOI resolution client
- `tools/semantic_scholar_client.py` — Semantic Scholar paper search API client
- `tools/openalex_client.py` — OpenAlex API client
- `tools/verification_cache.py` — SQLite-backed persistent cache for citation verification results
- `tools/citation_verification_summary.py` — per-citation verification status writer
- `tools/verify_passport.py` — CLI for citation verification gate
- `tools/uncited_assertion_detector.py` — detect uncited factual claims
- `tools/temporal_integrity_audit.py` — temporal verification audit for citations
- `tools/claim_audit_pipeline.py` — pipeline for claim alignment and drift audit
- `tools/policy_anchor_disclosure_referee.py` — policy anchor disclosure validation
- `tools/adapters/folder_scan.py` — literature corpus import from PDF folder
- `tools/adapters/zotero.py` — literature corpus import from Zotero Better BibTeX JSON
- `tools/adapters/obsidian.py` — literature corpus import from Obsidian vault

## Integration with research-first-reasoning meta-skill (Skill 7)

This skill integrates with the `research-first-reasoning` meta-skill (Skill 7) at two points:
1. **sub-gap-analyzer.md** Step 5: invokes Skill 7 to validate gap evidence against evidence hierarchy
2. **sub-quality-validator.md** Step 3: invokes Skill 7 to validate citation tier for major claims

When Skill 7 is not available, both sub-skills fall back to their built-in evidence hierarchy logic.

## Citation Verification Pipeline (v3.11 compatible)

The integrated citation verification tools (from academic-research-skills v3.11) provide:
- 4 API resolvers: ArXiv, Crossref, Semantic Scholar, OpenAlex
- SQLite cache with 90-day TTL for resolved metadata
- DOI-based deduplication
- Verification summaries per citation

---

## Cross-Skill Integration Notes

- `sub-gap-analyzer.md` invokes `Skill("research-first-reasoning")` at Step 5 for gap evidence validation
- `sub-quality-validator.md` invokes `Skill("research-first-reasoning")` at Step 3 for citation tier validation
- `main.md` invokes `Skill("research-first-reasoning")` at Step 3 to complement gap analysis
- All three integrations are optional (Skill 7 may not be installed) — each sub-skill has a built-in fallback that runs when Skill 7 is unavailable
- No circular dependency exists: Skill 7 is a stateless meta-skill that performs evidence evaluation, while research-paper-writer is a stateful harness

---

## Active Development Tasks

- [x] All phases complete — planning, implementation, testing, and cross-skill wiring done
- [x] Write `CLAUDE.md`
- [x] Write `PROJECT-detail.md`
- [x] Write `PROJECT-DEVELOPMENT-PHASE-TRACKING.md`
- [x] Write `SECOND-KNOWLEDGE-BRAIN.md`
- [x] Write `skills/main.md` + all 7 sub-skills
- [x] Write `tools/knowledge_updater.py`
- [x] Write `tests/test-scenarios.md`
- [x] Test knowledge_updater.py on 3 topic domains
- [x] Create `.claude/settings.json` with weekly cron schedule
- [x] Create automated test runner (`tests/run_test_scenario.py`)
- [x] Run all 7 test scenarios — all PASS
- [x] Integrate citation verification tools from academic-research-skills v3.11
- [x] Wire Skill 7 integration in sub-gap-analyzer, sub-quality-validator, main.md
- [x] Create `requirements.txt`, `requirements-dev.txt`, `.gitignore`
- [x] Create `announce-rpw-loaded.sh` SessionStart hook

---

## Related Files

- `PROJECT-detail.md` — full technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — build roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — domain knowledge base
- `shared/schemas/` — 23 JSON schemas for passport, audit, evaluation contracts
- `tests/test_results.md` — test execution results (all 7 scenarios pass)
