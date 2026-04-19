# Assignment 1 — Product description evaluation

Primary working notebook: **`assignment_01_notebook_v2.ipynb`** (Nebius API, OpenAI-compatible client).

## Goal

Learn an end-to-end **LLM evaluation** workflow: define quality **before** generating at scale, run a **baseline**, manually score a sample, try **targeted improvements**, then compare **human** ratings to an **LLM judge** with structured output.

## Business task

- **Input:** structured attributes per product (e.g. name, category, materials, dimensions).
- **Output:** a concise description suitable for a catalog or listing.
- **Risk:** models add plausible but **unsupported** details; the hardest requirement is usually **grounding** in the provided fields.

## Deliverables

- A clear **rubric** (Task 1) used consistently for manual eval and judge design.
- Generated descriptions and an **`assignment_01.xlsx`** export.
- A small **manual evaluation** and at least one **improvement experiment** with a short rationale.
- A **judge** with structured scores and a **comparison** to human labels.

## Environment

Use **Python 3.11+** with:

| Package | Role |
|--------|------|
| `pandas` | Load CSV, inspect rows, build the Excel artifact. |
| `openpyxl` | Write `.xlsx` for submission. |
| `openai` | OpenAI-compatible client for Nebius Studio API. |
| `pydantic` | Structured judge outputs (scores + rationale). |
| `tqdm` | Progress bars. |
| `jupyter`, `ipykernel`, `nbformat` | Notebook UI and kernel (local work). |

### Local setup (conda example)

```bash
conda create -n assignment01 python=3.11 -y
conda activate assignment01
conda install pandas openpyxl tqdm jupyter ipykernel nbformat -y
pip install pydantic openai python-dotenv
python -m ipykernel install --user --name assignment01 --display-name "Python (assignment01)"
```

Open this folder in Cursor or Jupyter Lab, open `assignment_01_notebook_v2.ipynb`, and select the **`Python (assignment01)`** kernel (or any kernel where the packages above are installed).

### API secrets

Set **`NEBIUS_API_KEY`** in the environment (see the notebook). Do not commit API keys.

You can use a **`.env`** file (not committed) with `NEBIUS_API_KEY`, and optionally `LLM_BASE_URL` / `LLM_MODEL`. The notebook loads `.env` from the assignment folder or up to two parent directories. Install **`python-dotenv`** (`pip install python-dotenv`) so that loading works.

## Data files

Place CSVs under **`data/`** (paths are relative to the notebook when you run it from this directory):

| File | Notes |
|------|--------|
| `data/01_agents_Assignment_01_product_dataset.csv` | Standard course set (~50 rows). |
| `data/Assignment_01_product_dataset_CHALLENGING.csv` | Optional harder set (~48 rows), same schema. |

**Colab:** upload the CSV and set `DATASET_PATH` in the notebook to match (e.g. `/content/01_agents_Assignment_01_product_dataset.csv`).

### Before generation — quick checks

1. Confirm **row count** and **column names**.
2. Spot-check rows for **missing values**, odd encodings, or **multi-value** fields.
3. Decide which columns are safe to quote vs need paraphrase (e.g. internal codes).

**Grounding checklist**

- Which fields are **authoritative** for factual claims (material, size, weight)?
- Which fields are **marketing-ish** and should not be treated as independent verification?
- Where data is **sparse**, the model should **not** fill gaps with guesses.

Keep a fixed **inspection sample** (row indices or product IDs) when comparing baseline vs improved prompts and when aligning the judge with humans.

### Dataset inspection — noise and hallucination risk

Both CSVs share schema: `product_name`, `Product_attribute_list`, `material`, `warranty`.

#### `01_agents_Assignment_01_product_dataset.csv` (standard)

**Noisy fields**

- **`Product_attribute_list`** — one long string mixes labeled chunks (`features:`, `dimensions:`, `rating:`, …) with vague tags (`compact`, `large`, `sustainably sourced`, …).
- **Template quirks** — some rows include **`battery: long-lasting`** even when misleading (e.g. consoles, LEGO, drinkware). Models may output bogus battery claims.
- **`product_name`** — relatively clean.
- **`material`** — short, fairly consistent.
- **`warranty`** — varies (1-year, 2-year, lifetime, …).

**Hallucination hotspots**

- Wrong or rounded **numeric specs** when paraphrasing.
- **Ratings** misquoted or applied to the wrong product.
- **Vague labels** turned into invented sizes or weights.
- **Features** invented when not in the string.
- **Battery claims** from erroneous `battery:` tails on non-battery-centric products.
- **Warranty** shortened or genericized.

#### `Assignment_01_product_dataset_CHALLENGING.csv`

**Noisy fields**

- **`Product_attribute_list`** — dense text with **`note:`** lines: **negations** (`does NOT`), limits, failure modes, timelines.
- **`warranty`** — multi-clause or exclusion-heavy; easy to over-summarize.

**Hallucination hotspots**

- **Negation errors** (saying the product **does** what attributes say it **does not**).
- **Omitted caveats** (subscriptions, filters not included, etc.).
- **Tone washing** — harsh notes softened into generic marketing.
- **Warranty overclaim** — broad coverage when the row limits it.
- **Prior knowledge vs row** — model defaults override explicit **`NOT`** in the data.

#### Comparison

| Aspect | Standard CSV | Challenging CSV |
|--------|--------------|-----------------|
| Main noise | Feature soup + vague tags + some bogus **`battery:`** tails | **`note:`** blocks with **negations** and timelines |
| Grounding difficulty | Align numbers/features with one messy field | Preserve **negations** and limits |
| Warranty | Usually one line | Often **exclusions** / carve-outs |

## Pedagogical notes

- **Rubric before generation:** If the rubric is unstable, you optimize for “sounds nice” instead of measurable criteria. The rubric is the contract for what “good” means.
- **Grounding:** Descriptions should only claim what attributes support; sparse data means stay general or say “not specified,” not invent facts.
- **Context engineering:** Prompts should pass the **right fields** in a consistent order; treat the dataframe as the single source of truth.
- **Evaluation-driven development:** Compare runs against the **same rubric** and sample.

## Other files

- `assignment_01_notebook_v1.ipynb` — earlier narrative-heavy version (reference).
- `docs/` — plans and prompts.
- `assignment_01_marimo.py` — optional Marimo-style workflow.
