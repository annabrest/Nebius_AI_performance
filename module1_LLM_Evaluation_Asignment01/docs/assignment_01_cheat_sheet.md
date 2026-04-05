# Assignment 1 Cheat Sheet

## Week 1 — Concepts you need

### 1. Base vs instruct vs chat models
- Base model: next-token completion only
- Instruct model: follows instructions
- Chat model: instruct model wrapped in message format

For this assignment, use instruct/chat-style prompting.

### 2. Prompt engineering
Goal: make the model produce the output you want with fewer mistakes.

Useful rules:
- be concise
- say what to do, not only what not to do
- clearly separate instructions from data
- specify the exact output target
- allow “don’t know” or “stay concise” instead of hallucinating
- structured output beats vague output requests

Applied here:
- ask for 50–90 words
- ask for friendly, credible sales tone
- forbid unsupported claims
- tell it to output only the description

### 3. Context engineering
Prompt engineering = wording the instruction.
Context engineering = everything the model sees:
- system prompt
- user prompt
- product data
- output schema
- previous turns
- tools

Applied here:
- your system prompt + product fields + judge schema = your context design

### 4. Tokens, cost, latency
Tokens affect:
- price
- context limit
- speed

Applied here:
- collect input tokens and output tokens
- compute cost per row
- measure latency_ms

### 5. Structured output
Instead of free text, constrain output to a schema.

Applied here:
- use Pydantic for the judge output
- explanation first, verdict second

### 6. Grounding
Grounding means the answer stays faithful to the provided input.

Applied here:
- the description must not invent features, benefits, specs, ratings, or materials
- grounding is your most important business criterion

### 7. Reasoning before label
Autoregressive models generate left to right.
If you ask for explanation before verdict, the model reasons first, then decides.

Applied here:
- judge schema should be:
  explanation
  verdict

## Week 2 — Concepts you need

### 8. EDD: Evaluation-Driven Development
Think of evals like tests for an AI system.

Loop:
1. define the behavior you want
2. define the eval
3. run baseline
4. inspect failures
5. improve prompt/model/params
6. rerun eval
7. decide whether to ship

Applied here:
- your rubric is the eval contract
- your experiments are judged by the eval, not vibes

### 9. A good eval has 4 parts
- fixed inputs
- scoring method
- comparison target
- decision it informs

Applied here:
- inputs = products
- scoring = human rubric or judge rubric
- comparison target = baseline vs improved version
- decision = keep baseline or switch

### 10. Metrics are proxies, not truth
One number can hide important failures.

Applied here:
- don’t use only pass rate
- inspect criterion-level results
- inspect examples where outputs got worse

### 11. Hidden stratification / slices
Average performance can look better while some groups do not improve.

Applied here:
- sample different product types
- compare categories if possible
- do not evaluate only the easiest items

### 12. Human evaluation
Pros:
- nuanced
- best for tone/helpfulness

Cons:
- slow
- expensive
- inconsistent

Applied here:
- evaluate 10–15 products manually

### 13. LLM-as-a-judge
Use another LLM to score outputs using your rubric.

Pros:
- scalable
- fast
- consistent

Cons:
- can be biased
- may reward verbosity
- can drift from your intended rubric

Applied here:
- use a strict judge prompt
- say “do not reward verbosity”
- be strict about grounding

### 14. Judge biases
Main ones from class:
- position bias
- verbosity bias
- self-enhancement bias

Applied here:
- use single-answer grading for rubric scoring
- constrain the rubric
- prefer checklist-like judging over vague “which is better?”

### 15. Sanity check before full run
Never trust a judge prompt immediately.

Applied here:
- run judge on 5 examples first
- inspect explanations manually
- adjust prompt if needed

### 16. Criterion-by-criterion judging
Judging all criteria at once can blur the rubric.
Judging one criterion at a time can improve focus.

Applied here:
- compare all-at-once vs one-criterion-per-call
- compute agreement with your human labels

### 17. Error analysis / buckets
Don’t stop at the score.
Group failures into buckets:
- hallucinated claims
- awkward phrasing
- wrong tone
- too short/too long
- overly generic copy

Applied here:
- your improvement ideas should target the biggest buckets

### 18. Reward hacking
If you optimize only the metric, the model may game the eval without getting truly better.

Applied here:
- don’t optimize only for pass rate
- keep grounding, tone, cost, and latency in view together

## What to say in your final reflection

### Human vs judge
- Human eval is best for nuance and trust
- Judge model is best for scale and consistency
- Production systems should use a hybrid:
  - automated judge for daily monitoring
  - programmatic checks for length/cost/latency
  - periodic human audit for calibration

### Best practical mindset
- baseline first
- improve one thing at a time
- compare fairly on the same sample
- inspect failures, not just averages