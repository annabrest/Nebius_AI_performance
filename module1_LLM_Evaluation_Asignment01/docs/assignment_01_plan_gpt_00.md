I reviewed the assignment, both lesson decks, and the product dataset. The assignment is well aligned with the course: it starts with prompt engineering and context design, then moves into evaluation-driven development, rubric design, human eval, LLM-as-a-judge, and comparison of metrics, cost, latency, and consistency.   

Here is the big picture:

Your assignment is not really about “writing product descriptions.” It is about learning to build an evaluation loop around an LLM system. That matches the course material very directly:

* Lesson 1 teaches prompt engineering, structured output, token economics, and context engineering. Those are exactly what you need for Tasks 1–2 and part of Task 5. 
* Lesson 2 teaches Evaluation-Driven Development: define the behavior, define the eval, measure quality/latency/cost, inspect failures, improve, and compare methods. That is exactly Tasks 1, 3, 4, 5, and 6. 

The dataset is small and manageable: 50 products with columns `product_name`, `Product_attribute_list`, `material`, and `warranty`. That is perfect for a first full evaluation loop. Some examples are electronics and accessories with semi-structured attributes like features, ratings, sustainability notes, and dimensions. That matters because “Grounding” will be one of the hardest criteria: the model may invent benefits or claims not present in those fields.

## How I recommend you approach it

Do it in 6 phases, matching the assignment.

### 1. First lock the rubric before generating anything

This is the most important step. If the rubric is vague, the rest becomes noisy.

A strong rubric should be:

* specific
* easy to apply repeatedly
* strict on grounding
* practical for later automation

A good starting rubric:

**Fluency**

* good: reads naturally, smooth sentence flow, no awkward phrasing
* ok: understandable but slightly awkward or repetitive
* bad: hard to read, choppy, unnatural, or confusing

**Grammar**

* good: no grammar, spelling, or punctuation issues
* ok: 1–2 minor issues that do not hurt understanding
* bad: multiple or noticeable grammar/spelling/punctuation errors

**Tone**

* good: friendly, credible, sales-oriented but not hypey
* ok: generally appropriate but bland, too generic, or slightly too promotional
* bad: off-brand, robotic, exaggerated, pushy, or not persuasive

**Length**

* good: 50–90 words
* ok: 40–49 or 91–110 words
* bad: under 40 or over 110 words

**Grounding**

* good: all claims are directly supported by provided fields
* ok: minor inference or marketing phrasing, but no clear factual invention
* bad: invents features, specs, ratings, benefits, certifications, or use cases not in input

**Latency**

* good: in your fastest bucket after measuring all rows
* ok: middle bucket
* bad: slowest bucket
  Since the assignment says average time per call, define this with thresholds after you do one baseline run.

**Cost**

* good: cheapest bucket among tested setups
* ok: moderate
* bad: expensive
  Same idea: define after baseline or by pricing tiers if you compare models.

Recommended pass/fail:

* pass if Grounding = good, Length ≠ bad, Grammar ≠ bad, and at least 4 criteria are good
* fail otherwise

Recommended automatic no-go:

* Grounding not good
* Length bad
* Grammar bad

Why this is a strong setup:

* It reflects the business goal
* It is strict where it matters
* It reduces judge ambiguity later

This part maps directly to Lesson 2’s message that an eval must inform a decision, not just produce a number. 

## 2. Build a baseline generation pipeline

For Task 2, do not over-optimize yet. First create a clean baseline with one of the required small models.

I would start with:

* `Meta-Llama-3.1-8B-Instruct`

Why start there:

* Usually reliable enough for controlled generation
* Small enough that bad outputs will still reveal failure modes
* Good baseline for later comparison

A good system prompt should follow the lesson guidance:

* concise
* positive instructions
* explicit structure
* explicit “don’t invent facts”
* explicit target tone
* explicit word range
* allow abstention only if needed

Example baseline system prompt:

```text
You are a careful e-commerce copywriter.

Write a persuasive product description in 50–90 words using only the provided product information.
Requirements:
- Keep the tone friendly, credible, and sales-oriented
- Use natural, fluent English
- Do not invent features, specs, ratings, materials, certifications, or use cases
- Mention concrete details from the input when possible
- If information is limited, stay concise rather than making assumptions
- Output only the final description
```

Why this is good:

* It follows Lesson 1 advice: concise system prompt, positive phrasing, explicit constraints, and “if unsure, don’t invent.” 
* It is optimized for grounding and tone, which are likely the key failure modes.

Then pass product-specific data in the user message in a clearly separated format:

```text
Product name: {product_name}
Attributes: {Product_attribute_list}
Material: {material}
Warranty: {warranty}

Write the product description now.
```

That follows the class guidance on separating instruction and data clearly. 

Collect for each row:

* generated_description
* latency_ms
* input_tokens
* output_tokens

Then save into `assignment_01.xlsx` with blank rubric columns.

## 3. Do manual evaluation on 10–15 products

Pick a balanced sample, not random-only.

I suggest sampling across slices such as:

* phones
* laptops
* headphones/earbuds
* wearables
* home devices

Why:
Lesson 2 emphasizes hidden stratification and slice analysis. If you only sample easy products, your baseline analysis will be misleading. 

When you evaluate manually, do two things:

* score criterion by criterion
* write short notes on failure modes

Typical failure buckets you will probably see:

* hallucinated use cases
* overly generic description
* too much marketing fluff
* length misses
* awkward phrasing from attribute stuffing

This is useful because Task 4 asks for an improvement cycle, and Lesson 2 explicitly says error analysis is the fastest path to real improvement. 

## 4. Improvement cycle: what to try and why

Do not try everything. Pick 2–3 meaningful experiments.

Best experiments for this assignment:

### Experiment A: Better prompt for grounding

Add stronger anti-hallucination language and maybe a lightweight output plan.

Example improvement:

```text
You are a careful e-commerce copywriter.

Write one product description in 50–90 words.
Use only the facts provided.
Do not add claims about performance, comfort, durability, compatibility, premium quality, or user benefits unless directly supported by the input.
Prefer concrete product facts over generic marketing language.
Keep the tone friendly and credible.
Output only the description.
```

Expected benefit:

* improves grounding
* reduces fluffy unsupported claims

Possible downside:

* may become drier and less persuasive
* could reduce tone quality

### Experiment B: Lower temperature

Try something like temperature 0.3 instead of 0.7.

Expected benefit:

* more deterministic
* fewer weird claims
* more consistent grammar and length

Possible downside:

* may become repetitive and generic

### Experiment C: Post-processing for length

If descriptions exceed 90 words, run a second pass:
“Shorten this to 50–90 words without changing facts.”

Expected benefit:

* easy fix for length failures

Possible downside:

* second pass adds latency and cost
* may accidentally remove useful detail or introduce drift

### Experiment D: Switch model

Try the other required model or a larger model only if justified.

Expected benefit:

* maybe better tone or fluency
* maybe better judge quality later

Possible downside:

* higher cost and latency
* stronger models can still hallucinate if prompt is weak

How to decide which experiment wins:
not just by average pass rate. Compare:

* grounding
* tone
* length compliance
* latency
* cost

That is exactly the EDD mindset from Lesson 2: always track quality, latency, cost, and safety together rather than chasing one number. 

## 5. Judge model design

This is the most conceptually important part.

Your judge should use:

* the original product fields
* the generated description
* your rubric definitions
* structured output via Pydantic

Exclude latency and cost from the judge because those are computed directly, which the assignment explicitly requires. 

### Why explanation should come before verdict

Because the lesson explains that reasoning before the label often improves classification quality in autoregressive models. Once the model commits to a label, it tends to justify it afterward. If it reasons first, the verdict is more likely to follow the rubric instead of being post-hoc rationalization. 

That is a strong answer for your writeup.

### Good judge design

Ask for per-criterion output like:

```python
class CriterionScore(BaseModel):
    explanation: str
    verdict: Literal["good", "ok", "bad"]
```

Then a full schema for:

* fluency
* grammar
* tone
* length
* grounding

### Important judge prompt design choice

Make the rubric concrete and checklist-like, not vague. Lesson 2 warns that LLM-as-a-judge suffers from position bias, verbosity bias, and rubric drift, so constrained evaluation is better. 

Example judge prompt idea:

```text
You are a strict evaluation judge for e-commerce product descriptions.

Score the description using only the rubric below.

Rubric:
Fluency:
- good: natural and smooth
- ok: understandable but somewhat awkward
- bad: unnatural or hard to read

Grammar:
...

Grounding:
- good: all claims are directly supported by the provided product data
- ok: minor inference but no clear invented facts
- bad: includes unsupported or invented claims

Evaluate the description against the product input.
Be strict about Grounding.
Do not reward verbosity.
Return structured output only.
```

Why “do not reward verbosity” matters:
because Lesson 2 explicitly calls out verbosity bias in LLM judges. 

## 6. Judge analysis: how to think about the results

This final part is where you show understanding, not just code.

### Human evaluation pros

* best for nuance
* better at catching subtle tone issues
* better at deciding whether copy “sounds convincing”
* can catch judge-model weirdness

### Human evaluation cons

* expensive
* slow
* inconsistent across raters
* hard to scale

### Judge model pros

* fast
* scalable
* consistent
* easy to rerun after every experiment

### Judge model cons

* biased toward certain styles
* may over-reward verbosity
* may misread grounding unless the prompt is very explicit
* can drift from your intended rubric

This directly matches Lesson 2’s discussion of LLM-as-a-judge and its limitations. 

### Production recommendation

For a system generating thousands of descriptions daily, I would recommend:

* use LLM-as-a-judge for continuous large-scale monitoring
* use programmatic checks for length, latency, cost, maybe simple grammar checks
* use periodic human audits on sampled outputs, especially failures and high-impact slices

That hybrid approach is the best production answer because:

* fully human does not scale
* fully judge-based is brittle
* hybrid gives both scale and calibration

## What this assignment helps you learn from the lessons

From Lesson 1, this assignment helps you learn:

* prompt engineering with concise, explicit prompts
* structured context formatting
* structured outputs
* token/cost awareness
* the difference between “good prompting” and real system design
* grounding and anti-hallucination prompting
* why context engineering matters more than prompt tricks alone. 

From Lesson 2, it helps you learn:

* how to define an eval before optimizing
* why average scores can hide failure modes
* how to connect metrics to decisions
* how to compare human evaluation and LLM-as-a-judge
* how to analyze deltas after prompt/model changes
* how to think in terms of cost, latency, scale, and consistency instead of just “quality”. 

## Bottlenecks you are likely to hit

### 1. Grounding ambiguity

The model will want to say things like “premium feel,” “ideal for busy professionals,” or “immersive listening.” Many of these are not explicitly in the input.

Pro:

* makes text sound better

Con:

* fails the business rule if you score grounding strictly

### 2. Tone vs. factuality tradeoff

The more persuasive you make the text, the more likely it invents benefits.

Pro:

* stronger marketing copy

Con:

* weaker grounding and trustworthiness

### 3. Judge inconsistency

Your judge may rate the same style differently depending on prompt wording.

Pro:

* automated scale

Con:

* hidden evaluation instability

### 4. Small-model generation quality

Since the required generation models are small, outputs may be bland or awkward.

Pro:

* great for learning error analysis
* easy to show improvement

Con:

* baseline may look messy

### 5. Overfitting to your rubric

You may optimize to pass your rubric rather than produce truly excellent descriptions.

Pro:

* good assignment performance

Con:

* classic EDD/reward-hacking risk, which Lesson 2 explicitly warns about. 

## A very practical submission strategy

For a strong assignment submission, I would structure it like this:

1. **Rubric**

   * table with good/ok/bad for each criterion
   * pass/fail rule
   * no-go rules

2. **Baseline generation**

   * chosen model
   * baseline prompt
   * decoding settings
   * saved spreadsheet

3. **Human evaluation**

   * evaluated sample of 10–15 products
   * scores by criterion
   * baseline analysis
   * top failure buckets

4. **Improvement cycle**

   * experiment 1
   * experiment 2
   * maybe experiment 3
   * short comparison table

5. **Judge model**

   * judge model choice
   * prompt
   * Pydantic schema
   * why explanation-before-verdict matters

6. **Judge results**

   * sanity check findings
   * full-run results
   * agreement with human labels
   * criterion-by-criterion judging vs all-at-once judging

7. **Reflection**

   * human vs judge trade-offs
   * production recommendation

## My advice on likely best-performing setup

If I were doing this assignment, I would start with:

* generation model: `Meta-Llama-3.1-8B-Instruct`
* baseline temperature: `0.3`
* concise grounding-focused system prompt
* manual eval on 12 products across categories
* first improvement: stricter anti-hallucination prompt
* judge model: the other small model first, then switch to a larger judge only if its reasoning is obviously weak

That gives you:

* a clean baseline
* visible improvement path
* enough contrast to discuss pros/cons intelligently

Two questions will help me guide you much more precisely:

1. Do you want help with the **writeup/report structure**, the **Python implementation**, or both?
2. Are you planning to run this in a **local notebook / Colab**, or do you want me to help you write it specifically for the **Nebius Token Factory / OpenAI-compatible API**?
