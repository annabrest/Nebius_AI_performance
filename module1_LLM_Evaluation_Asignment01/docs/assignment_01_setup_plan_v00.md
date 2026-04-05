Create these files exactly.

## 1. `.cursor/rules/00-project.mdc`

```md id="b7fq4p"
---
description: Core project context and working style for the Nebius assignment
globs:
alwaysApply: true
---

# Assignment context

This repository is for a Nebius AI performance engineering assignment submitted as a Jupyter notebook with outputs preserved.

## Primary goals
1. Produce a correct, runnable notebook for submission.
2. Help the student learn the Week 1 and Week 2 course material while building it.

## Working style
- Prefer small, auditable changes.
- Before major edits, briefly state the plan.
- When making design choices, explain trade-offs in plain English.
- Do not optimize for speed alone; optimize for learning and correctness.
- Keep the notebook understandable for someone who will review it later.

## Deliverables
- A notebook that runs top-to-bottom.
- Saved outputs embedded in the notebook.
- Clear markdown explanations for rubric, baseline, improvements, judge design, and analysis.

## Commands
Use these when relevant:
- `conda activate assignment01`
- `python -m ipykernel install --user --name assignment01 --display-name "Python (assignment01)"`
- `jupyter notebook`

## Constraints
- The final deliverable is a post-run `.ipynb` file with outputs visible.
- Prefer notebook-first work over building a large Python package.
- Keep code readable for a student still learning the material.
```

## 2. `.cursor/rules/10-learning-mode.mdc`

```md id="ts4q7s"
---
description: Make the assistant teach while helping
globs:
alwaysApply: true
---

# Learning mode

Teach while helping.

## When proposing a change
Always explain:
- what changed
- why it should help
- which Week 1 or Week 2 concept it relates to
- one downside or trade-off

## Concepts to connect back to

### Week 1
- prompt engineering
- context engineering
- grounding
- structured output
- token / cost awareness
- model choice
- temperature and generation controls

### Week 2
- evaluation-driven development
- rubric design
- human evaluation
- LLM-as-a-judge
- agreement analysis
- error buckets
- quality vs cost vs latency trade-offs

## Preferences
- Prefer short explanations over long lectures.
- Use concrete examples from the current notebook.
- Explain bottlenecks, pros, and cons.
- When editing prompts, explain which failure mode the prompt is targeting.

## Avoid
- black-box edits without explanation
- over-engineered abstractions
- doing everything automatically without showing reasoning
```

## 3. `.cursor/rules/20-notebook-workflow.mdc`

```md id="fsk8zd"
---
description: Notebook-specific workflow and structure
globs:
  - "*.ipynb"
alwaysApply: true
---

# Notebook workflow

This project is notebook-first.

## Preferences
- Prefer notebook cells over sprawling helper modules unless reuse is clearly needed.
- Add concise markdown before important code blocks.
- Keep each code cell focused on one step.
- Preserve outputs in the notebook.
- Before finalizing, make sure the notebook runs top-to-bottom.

## Notebook structure
Use sections in this order:
1. setup / imports
2. load data
3. rubric
4. baseline generation
5. save spreadsheet
6. manual evaluation
7. improvement experiments
8. judge model
9. judge analysis
10. final reflection

## Submission requirement
The final notebook must be post-run and contain outputs.

## Style
- Prefer clean, short cells.
- Avoid hiding core assignment logic in too many helper files.
- Keep markdown explanations practical and submission-ready.
```

## 4. `.cursor/rules/30-evaluation-driven-dev.mdc`

```md id="0lp6ch"
---
description: Enforce an evaluation-driven development mindset
globs:
alwaysApply: true
---

# Evaluation-driven development

Treat evaluation as the decision framework.

## Rules
- Do not propose prompt or model changes without naming the expected failure mode they address.
- Compare changes against a baseline.
- Prefer the same evaluation sample when comparing experiments.
- Track quality, cost, and latency together.
- For judge work, emphasize rubric alignment and grounding.

## Required analysis style
When evaluating results, report:
- what improved
- what got worse
- likely failure buckets
- whether the change is worth the trade-off

## Important
- Do not chase a single metric blindly.
- Do not treat pass rate as the only signal.
- Connect experiments to specific criteria such as grounding, tone, or length.
- Point out when a change may improve one criterion but hurt another.
```

## 5. `.cursor/rules/40-writing-report.mdc`

```md id="qrgs3a"
---
description: Keep writeups clear, concrete, and aligned with the assignment
globs:
alwaysApply: true
---

# Report writing

Write in a clear, engineering-focused style.

## Preferences
- Prefer short sections with explicit headings.
- Use concrete statements, not vague claims.
- For every experiment include:
  - what changed
  - why it was expected to help
  - what happened
  - pros
  - cons

## For judge-model sections
Always mention:
- why explanation comes before verdict
- likely judge biases
- why sanity check is necessary
- trade-offs vs human evaluation

## For reflections
Include:
- what the assignment taught from Week 1
- what the assignment taught from Week 2
- what bottlenecks were encountered
- what would be recommended in production
```

## 6. `.cursorignore`

```gitignore id="xxgo66"
.venv/
.env
.env.*
__pycache__/
*.xlsx
*.ipynb_checkpoints/
.DS_Store
```

## 7. Optional Skills

Only add these if your Cursor setup supports Skills well. Otherwise skip them for now.

### `.cursor/skills/assignment-planner/SKILL.md`

```md id="btgizx"
# Assignment planner

Use this skill when the user asks to plan, structure, or sequence work for the Nebius assignment.

## Goal
Break the assignment into concrete notebook tasks.

## Output format
Return:
1. ordered steps
2. what file/cell to edit
3. expected output artifact
4. concept learned from Week 1 or Week 2

## Preferences
- Keep steps practical
- Prefer one checkpoint per major task
- Mention likely bottlenecks
```

### `.cursor/skills/rubric-review/SKILL.md`

```md id="93b0ad"
# Rubric review

Use this skill when discussing evaluation criteria, pass/fail rules, or rubric wording.

## Tasks
- make rubric definitions less subjective
- spot ambiguity
- suggest stricter grounding language
- test whether another evaluator would likely agree

## Output format
For each criterion provide:
- risk of ambiguity
- suggested rewrite
- reason
- likely effect on human/judge agreement
```

### `.cursor/skills/judge-audit/SKILL.md`

```md id="klmbxh"
# Judge audit

Use this skill when reviewing judge prompts or structured outputs.

## Focus
- rubric drift
- verbosity bias
- weak grounding checks
- explanation-before-verdict ordering
- all-criteria-at-once vs one-criterion-per-call trade-offs

## Output format
Return:
- issue found
- why it matters
- prompt fix
- expected benefit
- possible downside
```

## 8. How to create them quickly in terminal

From your project root:

```bash id="sd8b9r"
mkdir -p .cursor/rules
mkdir -p .cursor/skills/assignment-planner
mkdir -p .cursor/skills/rubric-review
mkdir -p .cursor/skills/judge-audit
touch .cursorignore
```

Then paste each file content into the matching file.

## 9. The first 5 prompts I’d use in Cursor

```text id="9la4lv"
/plan Build the notebook section order for this assignment. For each section, explain which Week 1 or Week 2 concept it teaches.
```

```text id="kqug1n"
/ask Review my rubric. Which criteria are too subjective? Rewrite them to improve agreement between human evaluation and judge evaluation.
```

```text id="px3a1p"
/plan Compare two product-description prompts. Predict which criterion each one is most likely to improve or hurt.
```

```text id="akr9wz"
Audit my judge prompt for rubric drift, verbosity bias, and weak grounding checks. Suggest the smallest fixes first.
```

```text id="57i0su"
Review this notebook as a submission artifact. Check whether it clearly explains baseline, experiments, EDD, and judge-vs-human trade-offs.
```

## 10. My recommendation

Because your goal is both **submission + learning**, this setup is better than a minimal execution-only setup. It makes Cursor explain:

* why a prompt changed
* what criterion it affects
* how it maps to Week 1 or Week 2
* what trade-off you are making

That will help you learn the course material while building the assignment, instead of only outsourcing the work.

- `notes.md` template for the project with sections for rubric decisions, experiment log, judge observations, and final reflections.
