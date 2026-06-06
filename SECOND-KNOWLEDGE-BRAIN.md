# SECOND-KNOWLEDGE-BRAIN.md — research-paper-writer

> Self-improving domain knowledge base for academic research writing.
> Updated by `tools/knowledge_updater.py` on a weekly schedule.
> Last manual review: 2026-06-05

---

## Core Concepts & Frameworks

### Paper Structure Frameworks

**IMRaD (Introduction, Methods, Results, and Discussion)**
- Standard structure for empirical research papers in natural sciences, medicine, engineering
- Introduction: establishes context, problem, hypothesis
- Methods: reproducible description of what was done
- Results: objective presentation of findings without interpretation
- Discussion: interpretation, limitations, future work
- Used by: Nature, Science, IEEE, ACM, most biomedical journals

**Thematic / Narrative Review Structure**
- Used for literature reviews, survey papers, theoretical essays
- Typical sections: Abstract → Introduction → Background → Theme 1 → Theme 2 → Theme N → Synthesis → Conclusion
- Required when topic is conceptual rather than experimental

**PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)**
- Gold standard for systematic literature reviews
- Requires explicit search strategy, inclusion/exclusion criteria, PRISMA flow diagram
- Evidence level: highest in evidence hierarchy

---

### Evidence Hierarchy (Highest to Lowest)

| Rank | Evidence Type | Trust Level | Notes |
|------|--------------|-------------|-------|
| 1 | Systematic Review / Meta-Analysis | Highest | Synthesizes multiple RCTs |
| 2 | Randomized Controlled Trial (RCT) | Very High | Gold standard for causation |
| 3 | Cohort Study (Prospective) | High | Good for long-term outcomes |
| 4 | Case-Control Study | Moderate | Good for rare outcomes |
| 5 | Cross-Sectional Study | Moderate | Good for prevalence |
| 6 | Expert Opinion / Consensus Statement | Low-Moderate | No original data |
| 7 | Blog / News / Opinion Piece | Low | Not peer-reviewed |

The skill enforces: cite higher-tier evidence first; if only lower-tier available, explicitly flag limitation.

---

### Citation Style Reference

**APA 7th Edition (default)**
- Format: Author, A. A., & Author, B. B. (Year). Title. *Journal*, *Volume*(Issue), pages. DOI
- In-text: (Author, Year) or Author (Year)

**IEEE**
- Format: [N] A. Author, "Title," *Journal*, vol. V, no. N, pp. X–Y, Mon. Year, doi: XXX
- In-text: [N] numbered reference

**MLA 9th Edition**
- Format: Author, First. "Title." *Journal*, vol. V, no. N, Year, pp. X–Y. DOI/URL.
- In-text: (Author page)

---

### Gap Analysis Methodology

A knowledge gap must meet ALL three criteria:
1. **Absence evidence**: ≥2 papers state the question is open, unexplored, or limited
2. **Relevance**: The gap is directly related to the user's paper topic
3. **Addressability**: The paper can contribute to narrowing the gap (via synthesis, analysis, or argument)

Common gap categories:
- **Population gap**: Study conducted in one population, not generalized
- **Temporal gap**: Only older studies available; recent data missing
- **Methodological gap**: Existing studies use weaker designs; stronger evidence needed
- **Conceptual gap**: Theoretical framework underdeveloped
- **Replication gap**: Key findings not replicated across contexts

---

## Key Research Papers

### Academic Writing & Research Methodology

| Title | Authors | Year | Venue | DOI/Link | Relevance |
|-------|---------|------|-------|---------|---------|
| How to Write a Research Paper | N. Alexandrov | 2023 | arXiv | https://arxiv.org/abs/2312.01952 | General research writing guide |
| The PRISMA 2020 Statement | Page et al. | 2021 | PLOS Medicine | 10.1371/journal.pmed.1003583 | Systematic review standard |
| Writing Science: How to Write Papers That Get Cited | Schimel | 2012 | Oxford UP | ISBN 9780199760244 | Narrative structure for science writing |
| Automated Scientific Paper Review | Liu et al. | 2023 | ACL | 10.18653/v1/2023.acl-long.638 | AI for paper review |
| SciSpace: AI Research Paper Assistant | Typeset | 2024 | Product | https://typeset.io | AI-assisted academic writing tooling |

### LLM-Assisted Academic Writing

| Title | Authors | Year | Venue | DOI/Link | Relevance |
|-------|---------|------|-------|---------|---------|
| GPT-4 for Scientific Writing | Lund & Wang | 2023 | Learned Publishing | 10.1002/leap.1570 | LLM capabilities for academic text |
| The AI Scientist: Towards Fully Automated Scientific Discovery | Lu et al. | 2024 | arXiv | https://arxiv.org/abs/2408.06292 | End-to-end AI paper generation |
| Do LLMs Produce Faithful Citations? | Huang et al. | 2024 | ACL Findings | 10.18653/v1/2024.findings-acl.273 | Citation hallucination risk |
| STORM: Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking | Shao et al. | 2024 | NAACL | 10.18653/v1/2024.naacl-long.347 | LLM outline generation |
| Multi-Agent Framework for Scientific Paper Writing | Wang et al. | 2024 | arXiv | https://arxiv.org/abs/2404.01644 | Multi-agent academic writing harness |

---

## State-of-the-Art Methods & Tools

### Literature Search APIs

| Tool | API | Coverage | Rate Limit |
|------|-----|----------|-----------|
| Semantic Scholar | api.semanticscholar.org/graph/v1 | 200M+ papers | 100 req/5min (free) |
| ArXiv | export.arxiv.org/api/query | CS, Physics, Math, Econ, Bio | No official limit |
| PubMed E-utilities | eutils.ncbi.nlm.nih.gov | 35M biomedical | 10 req/sec (with API key) |
| CrossRef | api.crossref.org/works | 130M+ DOI records | Polite pool: unlimited |
| OpenAlex | api.openalex.org | 250M+ works | 100k req/day (free) |

### Citation Style Processors

| Tool | Languages | Styles Supported |
|------|-----------|-----------------|
| citation-js | JavaScript/Node | APA, MLA, IEEE, Chicago + 10,000+ CSL styles |
| citeproc-py | Python | Any CSL-compatible style |
| pybtex | Python | BibTeX/BibLaTeX |
| anystyle | Ruby | Parses unstructured references |

### Academic Paper Structure Checkers

| Tool | Purpose |
|------|---------|
| sciscore.com | Reproducibility/rigor score for methods sections |
| statcheck.io | Automated NHST statistics verification |
| LanguageTool | Grammar and academic style checker |

---

## Authoritative Data Sources

| Source | URL | Purpose |
|--------|-----|---------|
| ArXiv | https://arxiv.org | Preprint server: CS, Physics, Math, Bio, Econ |
| Semantic Scholar | https://www.semanticscholar.org | AI-enhanced paper search + citation graph |
| PubMed | https://pubmed.ncbi.nlm.nih.gov | Biomedical and life sciences |
| CrossRef | https://www.crossref.org | DOI resolution and metadata |
| OpenAlex | https://openalex.org | Open catalog of scholarly works |
| CORE | https://core.ac.uk | Open access research aggregator |
| DOAJ | https://doaj.org | Directory of open access journals |
| Unpaywall | https://unpaywall.org | Find free legal versions of papers |

---

## Analytical Frameworks (from Skill 7 — research-first-reasoning)

Applicable methods from the 40-method library for this domain:

| Method | Application in research-paper-writer |
|--------|--------------------------------------|
| Systematic Review | Stage 1: structure literature discovery |
| Gap Analysis | Stage 2: identify research gaps in bibliography |
| Devil's Advocate | Stage 2: challenge gap hypotheses before accepting |
| Evidence Hierarchy | Stage 7: rank citations by evidence type |
| Thematic Synthesis | Stage 3: group papers by theme for outline |
| Argument Mapping | Stage 4: structure logical flow of each section |
| Peer Review Simulation | Stage 5: cross-review protocol |
| Counterfactual Reasoning | Stage 2: "what if this gap doesn't matter?" |
| Citation Network Analysis | Stage 6: identify most-cited foundational papers |

---

## Self-Update Protocol

**Crawl sources:**
```
arxiv: cs.AI, cs.CL, cs.LG, stat.ML, q-bio.GN, econ.GN
semantic_scholar: query="{topic}" sort=citationCount date={last_90_days}
pubmed: query="{topic}" filter=last_1_year sort=relevance
```

**Scoring formula:**
```python
score = (recency_score * 0.3) + (relevance_score * 0.5) + (citation_score * 0.2)
# recency_score: 1.0 if <30 days, 0.8 if <90 days, 0.5 if <1 year, 0.2 if <3 years
# relevance_score: keyword match count / total keywords (0.0–1.0)
# citation_score: min(citations / 100, 1.0)
```

**Append format:**
```markdown
| Title | Authors | Year | Venue | DOI/Link | Score | Added |
|-------|---------|------|-------|---------|-------|-------|
| {title} | {authors} | {year} | {venue} | {doi} | {score:.2f} | {date} |
```

**Deduplication:** SHA-256 hash of DOI string; skip if hash already in index.

**Run schedule:** Weekly (Sunday 02:00 UTC)

---

## Knowledge Update Log

| Date | Source | Papers Added | Domains | Operator |
|------|--------|-------------|---------|----------|
| 2026-06-05 | Manual bootstrap | 10 | Academic writing, LLM writing tools | System init |


<!-- Auto-appended by knowledge_updater.py on 2026-06-06 | topic: transformer attention mechanisms NLP -->
| Vortex: Efficient and Programmable Sparse Attention Serving for AI Age | Zhuoming Chen et al. | 2026 | arXiv preprint | https://arxiv.org/abs/2606.06453v1 | 0.42 | 2026-06-06 |
| You Only Index Once: Cross-Layer Sparse Attention with Shared Routing | Yutao Sun et al. | 2026 | arXiv preprint | https://arxiv.org/abs/2606.06467v1 | 0.36 | 2026-06-06 |
| Revising Context, Shifting Simulated Stance: Auditing LLM-Based Stance | Xinnong Zhang et al. | 2026 | arXiv preprint | https://arxiv.org/abs/2606.06443v1 | 0.36 | 2026-06-06 |

<!-- Log: | 2026-06-06 | ArXiv | 3 | transformer attention mechanisms NLP | Auto-crawl |
 -->
