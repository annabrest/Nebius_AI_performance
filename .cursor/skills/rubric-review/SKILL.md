---
name: rubric-review
description: Tightens evaluation rubrics for clarity, grounding, and inter-rater agreement. Primary context module1_LLM_Evaluation_Asignment01/. Use when discussing criteria, pass/fail rules, rubric wording, or human vs judge alignment for that assignment or similar eval work.
---

# Rubric review

## When to use

Apply when discussing evaluation criteria, pass/fail rules, rubric wording, or scoring definitions.

## Tasks

- Make rubric definitions less subjective where possible.
- Spot ambiguity and unstated assumptions.
- Suggest stricter **grounding** language when claims must be supported by inputs.
- Test whether another evaluator would likely agree given the text alone.

## Output format

For **each criterion**, provide:

| Field | Content |
|-------|---------|
| Risk of ambiguity | What could be read two ways or overfit to one example style |
| Suggested rewrite | Concrete replacement wording |
| Reason | Why the rewrite reduces disagreement |
| Effect on agreement | Likely impact on human/human and human/judge agreement |

Keep rewrites minimal unless the criterion is fundamentally unclear.

## Preferences

- Prefer observable signals (what to check in the model output) over vibes.
- If a criterion mixes multiple judgments, flag **split criterion** as an option.
