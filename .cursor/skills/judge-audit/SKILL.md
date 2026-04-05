---
name: judge-audit
description: Audits LLM-as-judge prompts and structured judge outputs for rubric drift, bias, and grounding. Primary context module1_LLM_Evaluation_Asignment01/. Use when reviewing judge prompts, schemas, or verdict pipelines for that assignment or similar judge setups.
---

# Judge audit

## When to use

Apply when reviewing judge prompts, judge system messages, structured judge outputs, or comparing judge design to the human rubric.

## Focus areas

- **Rubric drift**: judge optimizes for something not in the rubric (length, confidence tone, formatting).
- **Verbosity bias**: longer answers rated higher without evidence.
- **Weak grounding checks**: verdicts not tied to quotes or explicit checks against source material.
- **Explanation-before-verdict**: reasoning must precede the final pass/fail or score to reduce post-hoc rationalization.
- **All-criteria-at-once vs one-criterion-per-call**: trade-offs for cost, latency, error isolation, and consistency.

## Output format

For each issue:

1. **Issue** — what is wrong, with a short quote or pointer to the prompt/schema.
2. **Why it matters** — how it skews scores or human/judge agreement.
3. **Prompt fix** — smallest change first; escalate only if needed.
4. **Expected benefit** — what should improve (e.g. grounding, stability, agreement on edge cases).
5. **Possible downside** — cost, latency, fragility, or new failure mode.

## Preferences

- Prefer **smallest** prompt or schema edits before redesigning the whole judge.
- If suggesting structured output, ensure fields force evidence before verdict where the rubric requires it.
