Here’s the cleanest way to start the assignment **from scratch**, as if you were building it yourself in Cursor and Jupyter, not relying on the notebook I made.

A Jupyter notebook is a `.ipynb` file that stores your code, markdown, metadata, and outputs together, and the code actually runs in a separate long-running **kernel** process. That is why variables persist across cells until you restart the kernel. ([docs.jupyter.org][1])

## Phase 0: Set up your workspace once

### Step 1: Create a project folder

Make one folder for the whole assignment, for example:

```text id="v4oj3d"
assignment_01/
```

Put inside it:

* the dataset CSV
* your notebook
* optional notes file
* `.cursor/` rules if you want Cursor guidance

### Step 2: Create your Python environment

Since you want conda, do:

```bash id="xdy0tv"
conda create -n assignment01 python=3.11 -y
conda activate assignment01
pip install pandas openpyxl pydantic openai tqdm jupyter ipykernel nbformat
```
or

```bash
conda create -n assignment01 python=3.11 -y
conda activate assignment01
conda install pandas openpyxl tqdm jupyter ipykernel nbformat -y
pip install pydantic openai
``` 


### Step 3: Register the environment as a Jupyter kernel

This is what makes your environment show up inside the notebook UI:

```bash id="gw96is"
python -m ipykernel install --user --name assignment01 --display-name "Python (assignment01)"
```

### Step 4: Open the folder in Cursor

Then open your notebook or create a new `.ipynb`.

### Step 5: Select the kernel

In the notebook UI, choose:

```text id="b0gpse"
Python (assignment01)
```

If the wrong kernel is selected, imports may fail even if you installed everything in the correct conda environment. Jupyter kernels are the processes that run notebook code, while the notebook file itself is just the saved document. ([docs.jupyter.org][2])

## Phase 1: Create the notebook skeleton

### Step 6: Create notebook sections before writing code

Start with markdown headers only.

Use this structure:

```text id="imx2m3"
1. Title and assignment goal
2. Setup / imports
3. Load dataset
4. Task 1 - rubric
5. Task 2 - baseline generation
6. Save assignment_01.xlsx
7. Task 3 - manual evaluation
8. Task 4 - improvement experiment(s)
9. Task 5 - judge model
10. Task 6 - judge analysis
11. Final reflection
```

Why this order:

* it matches the assignment flow
* it keeps the notebook readable
* it helps you think in EDD order: define eval, run baseline, inspect, improve, automate

## Phase 2: Start with understanding, not generation

### Step 7: Read the assignment and summarize it in one markdown cell

Write, in your own words:

* what the business task is
* what the criteria are
* what artifacts you must submit

This helps you avoid coding before understanding.

### Step 8: Inspect the dataset

In a code cell:

* load the CSV with pandas
* show `head()`
* check column names
* check row count
* inspect 3–5 products manually

At this stage, your goal is to understand:

* how structured the attributes are
* what fields are noisy
* what kinds of claims a model might hallucinate

This matters because **grounding** will likely be your hardest criterion.

## Phase 3: Do Task 1 first — rubric

### Step 9: Write the rubric before generating anything

Create one markdown cell with the full rubric:

* fluency
* grammar
* tone
* length
* grounding
* latency
* cost

For each, define:

* good
* ok
* bad

Then define:

* pass/fail rule
* automatic no-go rules

Do not skip this. This is the foundation of the whole assignment.

A good way to think:

* **Length** should be objective
* **Grounding** should be strict
* **Tone** should be specific enough that another person could apply it too

### Step 10: Add a code cell with your rubric as Python objects

Put the same rubric into a dictionary in code.
This will help later when you build the judge prompt.

This is your first direct connection to Week 2:

* eval before optimization
* criteria before experimentation

## Phase 4: Build the baseline generation pipeline

### Step 11: Configure your API client

Add a setup cell for:

* API key
* base URL
* model name

Use a notebook-safe input for secrets, like `getpass`, so you do not hardcode credentials in the notebook.

### Step 12: Write a baseline system prompt

Do not try to be clever yet.

Your baseline prompt should:

* ask for 50–90 words
* ask for friendly, credible sales tone
* forbid invented facts
* ask for output only

Then create a helper function that formats the product fields into a user prompt.

### Step 13: Test generation on 3 rows only

Before running the whole dataset, test on a tiny slice.

Why:

* catch model ID problems
* catch API formatting mistakes
* check the prompt quality fast
* avoid wasting tokens

Look at the 3 descriptions manually and ask:

* are they within length?
* do they invent facts?
* are they too generic?
* do they sound salesy in a good way or too hypey?

### Step 14: Add latency and token capture

For each generation call, collect:

* `generated_description`
* `latency_ms`
* `input_tokens`
* `output_tokens`

This is important because the assignment explicitly asks for those fields, and Week 1 emphasizes tokens, cost, and context as real engineering constraints.  

### Step 15: Run on all products

Once the 3-row test looks good, run the full dataset.

Then build a dataframe that includes:

* original product fields
* generated description
* latency
* token counts
* empty columns for manual scores
* empty `final_score`

### Step 16: Save `assignment_01.xlsx`

This completes the core of Task 2.

## Phase 5: Do manual evaluation

### Step 17: Add cost calculation

Find the pricing for your chosen model and compute row-level cost from:

* input tokens
* output tokens

Then create a `cost_usd` column.

### Step 18: Pick 10–15 products for human evaluation

Do not just pick the first 10.

Pick a mix of product types if possible:

* audio
* phones
* laptops
* accessories
* wearables
* home devices

That gives you a better sample and helps you avoid hidden stratification, which Week 2 warns about. 

### Step 19: Score each selected row manually

For each of the 10–15 rows, assign:

* fluency
* grammar
* tone
* length
* grounding

Then apply your pass/fail logic.

### Step 20: Write baseline analysis notes

Create a markdown cell answering:

* which criteria performed best?
* which performed worst?
* what failure buckets did you notice?

Typical buckets might be:

* hallucinated benefits
* too generic
* awkward phrasing
* too short / too long
* tone too bland

This is the moment where you convert scores into learning.

## Phase 6: Improvement cycle

### Step 21: Pick one meaningful change

Do not do five experiments at once.

Pick one change and justify it.

Best first options:

* stricter grounding prompt
* lower temperature
* stronger tone guidance
* length-focused second pass

### Step 22: State the hypothesis before coding

In markdown, write:

* what changed
* why you think it should help
* which criterion it targets
* what downside you expect

That is pure EDD thinking.

### Step 23: Run the experiment

Generate descriptions again with the changed setup.

### Step 24: Re-score the same manual sample

Use the same 10–15 rows you already evaluated.

This keeps the comparison fair.

### Step 25: Compare baseline vs experiment

Write:

* what improved
* what got worse
* whether the trade-off is worth it

That matters because Week 2 stresses that you should evaluate quality, latency, cost, and risk together, not chase one number. 

## Phase 7: Build the judge model

### Step 26: Start with the other model family

Per the assignment, use the model you did not use for generation first. 

### Step 27: Create a Pydantic schema

Make a schema with one object per criterion:

* explanation
* verdict

Put **explanation before verdict**.

Why this ordering matters:
the lesson explains that for classification-like tasks, asking the model to reason before giving the label is better than asking for the label first and explanation later. 

### Step 28: Write the judge prompt

Include:

* your rubric definitions
* instruction to use product fields as source of truth
* instruction to be strict about grounding
* instruction not to reward verbosity

That last point matters because Week 2 explicitly warns about verbosity bias in LLM judges. 

### Step 29: Sanity check on 5 rows

Do not run the full dataset yet.

Inspect:

* are explanations sensible?
* does grounding use the product input properly?
* is the judge too generous?
* is it confusing tone with fluency?

Only after that should you do the full run.

## Phase 8: Judge full run and comparison

### Step 30: Run the judge on all products

Store:

* explanation and verdict for each criterion
* judge-based final score

### Step 31: Compare judge vs human labels

For the rows you manually scored, compute agreement by criterion.

You want answers like:

* high agreement on length
* medium agreement on grammar
* weaker agreement on tone and grounding

Then explain why.

### Step 32: Try criterion-by-criterion judging

Run the judge separately for each criterion.

Then compare whether agreement improved.

A likely pattern:

* isolated judging may improve focus
* but it costs more and is slower

That is a good discussion point because it directly reflects the trade-off mindset from Week 2.

## Phase 9: Final reflection and submission prep

### Step 33: Add a reflection section

Answer:

* what did you learn from Week 1?
* what did you learn from Week 2?
* what was the biggest bottleneck?
* what would you recommend for production?

A strong production recommendation is usually:

* automated judge for scale
* programmatic checks for length/cost/latency
* periodic human audit for calibration

### Step 34: Restart kernel and run all

Before submission, do the notebook hygiene step:

* restart kernel
* run all cells from top to bottom
* confirm no hidden dependency on stale state

Because notebooks store outputs in the `.ipynb` file when saved, the safe final workflow is: run all, verify outputs are visible, then save the notebook. Jupyter’s documentation notes that notebooks store code, content, and outputs in the `.ipynb` file when saved. ([docs.jupyter.org][1])

### Step 35: Save and reopen the notebook

This is your final validation:

* close notebook
* reopen it
* confirm outputs are still there

If they are, the submission file is in good shape.

---

## The shortest possible “start now” version

If you want the absolute minimum starter sequence:

1. create folder
2. create conda env
3. install packages
4. register kernel
5. open notebook in Cursor
6. select kernel
7. load CSV
8. inspect dataset
9. write rubric
10. write baseline prompt
11. test on 3 rows
12. run full dataset
13. save `assignment_01.xlsx`
14. manually score 10–15 rows
15. run one experiment
16. build judge schema + prompt
17. sanity check on 5 rows
18. full judge run
19. compare with human scores
20. restart kernel, run all, save, submit

## The main mindset to keep

Do not think:
“Now I need to generate descriptions.”

Think:
“I am building an evaluation pipeline around a generation task.”

That is the real assignment.


[1]: https://docs.jupyter.org/en/stable/projects/architecture/content-architecture.html?utm_source=chatgpt.com "Architecture - Project Jupyter Documentation"
[2]: https://docs.jupyter.org/en/latest/what_is_jupyter.html?utm_source=chatgpt.com "What is Jupyter?"
