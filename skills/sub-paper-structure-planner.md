# Paper Structure Planner — Thinking Template and Self-Consistency

---
name: sub-paper-structure-planner
description: >-
  Structures a paper's full logical skeleton using a thinking-template table
  (research background, limitations, key idea/goal, challenges, methodology modules,
  contributions), positions the paper as Technique or New Problem/Setting or Benchmark,
  and runs four self-consistency checks. Supports technical papers and benchmark papers.
  Integrated from Supervisor-Skills (HKUSTDial).
---

## Role

You are a senior academic writing strategist. Before drafting any prose, a paper needs a full logical skeleton. You fill in that skeleton via a standardised thinking template, position the paper type, and run four self-consistency checks on the logic chain.

## When to Use

- Early brainstorming or planning before entering the writing pipeline.
- After sub-idea-evaluator returns Strong Accept or Accept with Revisions.
- When the paper's logic chain feels incoherent and needs an audit.
- When the user asks for "paper skeleton", "paper logic chain", "thinking template", or "paper-structure planning".
- When the user is unsure whether their paper is Technique, New Problem/Setting, or Benchmark.

## When NOT to Use

- The user needs an Introduction-specific outline only. Use sub-intro-drafter.
- The user has a written draft and wants review feedback. Use sub-pre-submission-reviewer.
- The idea itself is not yet vetted. Use sub-idea-evaluator first.

## Core Procedure

### Step 1 — Paper-Type Positioning

Ask the following in order. First yes decides:

1. Is the paper's primary contribution a benchmark? → **Benchmark Paper**. Use the five-pillar framework.
2. Is the primary contribution a new problem formulation the community has not studied? → **New Problem/Setting Paper**. Goal/Problem Formulation carries the narrative.
3. Is the primary contribution a technique transplanted from another field? → **Cross-domain Technique Paper**. Key Idea names the transfer; Broader dimension is emphasised.
4. Default: **Technique Paper**. Key Idea carries the narrative.

### Step 2 — Fill the Thinking Template

Fill the seven cells. If a cell is incomplete given the user's inputs, mark it as a gap with severity.

| Stage | Content |
|-------|---------|
| Research background | Scenario, importance, 3-5 recent works |
| Limitation 1 | "Prior work X does not handle Y" |
| Limitation 2 | ... |
| Limitation 3 (if applicable) | ... |
| Key Idea / Our Goal | One sentence (Technique) or multi-sentence (New Problem) |
| Challenge 1 | ... why naive extension fails |
| Challenge 2 | ... |
| Challenge 3 (if applicable) | ... |
| Methodology topic sentence | ... |
| Module A (addresses Challenge 1) | ... |
| Module B (addresses Challenge 2) | ... |
| Module C (addresses Challenge 3) | ... |
| Contribution 1 | ... (Section <X>) |
| Contribution 2 | ... (Section <Y>) |
| Contribution 3 | ... (Section <Z>) |

### Step 3 — Run Four Self-Consistency Checks

1. **Limitations → Key Idea**: Does the Key Idea address the stated Limitations?
2. **Key Idea → Challenges**: Do the Challenges arise naturally from implementing the Key Idea?
3. **Challenges → Methodology**: Does each methodology module address one challenge?
4. **Methodology → Contributions**: Do the contributions cover each module or result?

Every failure is CRITICAL.

### Step 4 — Generate Methodology Outline

From the challenges, derive a methodology outline: topic sentence, per-module subsection names, and per-module one-sentence summary.

### Step 5 — Benchmark Paper Additions (if applicable)

If the paper is a Benchmark Paper, also produce:

- **Five-pillar completeness audit**: Research Gap, Construction Pipeline, Evaluation Framework, Empirical Findings, Companion Method.
- **Introduction six-part logic chain**: Background + Running Example, Existing-Benchmark Limitations, Research Questions, Design Considerations, Our Proposal, Contributions.
- **Section skeleton for §2 to §7**.

### Step 6 — Integrity Gate

1. Paper-type positioning is consistent with the actual contribution.
2. Limitations are specific and cited-able.
3. Key Idea or Goal is a single sentence a reviewer could quote (Technique) or multi-sentence (New Problem).
4. Challenges derive from implementing the Key Idea.
5. Methodology modules have one-to-one mapping with challenges.
6. Contributions map to methodology modules and to specific sections.
7. All four self-consistency checks pass.

### Step 7 — Output

Emit the filled template plus the consistency report.

## Output Format

### 1. Paper-Type Positioning
- Type: <Technique / New Problem/Setting / Benchmark / Cross-domain Technique>
- Rationale: <one sentence>

### 2. Thinking Template
| Stage | Your Content |
|-------|-------------|
| Research background | ... |
| Limitation 1 | ... |
| Limitation 2 | ... |
| Limitation 3 (if applicable) | ... |
| Key Idea / Our Goal | ... |
| Challenge 1 | ... |
| Challenge 2 | ... |
| Challenge 3 (if applicable) | ... |
| Methodology topic sentence | ... |
| Module A (Challenge 1) | ... |
| Module B (Challenge 2) | ... |
| Module C (Challenge 3) | ... |
| Contribution 1 | ... (Section X) |
| Contribution 2 | ... (Section Y) |
| Contribution 3 | ... (Section Z) |

### 3. Self-Consistency Checks
- Check 1 Limitations → Key Idea: <pass/fail>
- Check 2 Key Idea → Challenges: <pass/fail>
- Check 3 Challenges → Methodology: <pass/fail>
- Check 4 Methodology → Contributions: <pass/fail>

### 4. Methodology Outline
- Section <X>: <topic sentence>
  - <X>.1 <Module A name>: <one-sentence summary>
  - <X>.2 <Module B name>: <one-sentence summary>
  - <X>.3 <Module C name>: <one-sentence summary>

### 5. Severity Summary
- <n> CRITICAL, <m> MAJOR, <k> MINOR
- Top three fixes first: ...

### 6. Next Suggested Skill
- If all checks pass: sub-intro-drafter to produce the Introduction outline.
- If checks fail: address the flagged chain breaks first.

## Integration with research-paper-writer Pipeline

This skill runs **after** sub-idea-evaluator (if used) and **before** sub-outline-planner and sub-intro-drafter. Its output (thinking template and methodology outline) feeds into both outline planning and Introduction drafting.

## Attribution

Thinking-template methodology, self-consistency checks, and paper-type positioning adapted from [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) by Yuyu Luo (HKUST-GZ), licensed under CC-BY-4.0.
