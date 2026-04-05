---
name: assignment-planner
description: Breaks the Nebius LLM evaluation assignment into ordered notebook tasks with checkpoints and course links. Primary path module1_LLM_Evaluation_Asignment01/. Use when planning or sequencing that assignment or a similar notebook-first eval project in this monorepo.
---

# Assignment planner

## When to use

Apply when planning, structuring, or sequencing work for the Nebius assignment under `module1_LLM_Evaluation_Asignment01/` (notebook-first, evaluation-driven).

## Goal

Break the assignment into concrete notebook tasks.

## Output format

Return:

1. Ordered steps
2. What file or cell to edit
3. Expected output artifact (e.g. spreadsheet, table, saved model outputs)
4. Which **Week 1** or **Week 2** concept the step reinforces

## Preferences

- Keep steps practical and small enough to verify in one sitting when possible.
- Prefer one checkpoint per major task (runnable cell, saved artifact, or clear markdown milestone).
- Call out likely bottlenecks (API limits, cost, latency, manual eval time, judge alignment).

## Week 1 / Week 2 anchors (for step 4)

- **Week 1**: prompts, context, grounding, structured output, tokens/cost, model choice, temperature and sampling controls.
- **Week 2**: evaluation-driven development, rubric design, human eval, LLM-as-judge, agreement, error buckets, quality vs cost vs latency.
