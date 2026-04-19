import marimo

__generated_with = "0.22.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Assignment 1 — Product description evaluation

    ## Goal: learn LLM evauation process

    Build and evaluate **short product descriptions** from structured product data: define quality **before** generating at scale, run a **baseline**, manually score a sample, try **targeted improvements**, then compare **human** ratings to an **LLM judge** with structured output.

    ## Business task (in my own words)

    - **Input:** structured attributes per product (e.g. name, category, materials, dimensions).
    - **Output:** a concise description suitable for a catalog or listing.
    - **Risk:** models easily add plausible but **unsupported** details; the hardest requirement is usually **grounding** in the provided fields.

    ## Deliverables this notebook supports

    - A clear **rubric** (Task 1) used consistently for manual eval and judge design.
    - Generated descriptions and an **`assignment_01.xlsx`** export.
    - A small **manual evaluation** and at least one **improvement experiment** with a short rationale.
    - A **judge** with structured scores and a **comparison** to human labels.

    > **Week 2 idea — rubric before generation:** If we generate before the rubric is stable, we optimize for “sounds nice” instead of measurable criteria. The rubric is the contract for what “good” means.

    > **Week 1 idea — grounding:** Descriptions should only claim what the attributes support; vague or missing attributes are a signal to stay general or say “not specified,” not to invent facts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup and imports

    **Environment:** Python 3.11+ with `pandas`, `openpyxl` (Excel), `openai` (API), `pydantic` (structured schemas), `tqdm` (progress). Kernel must match the env where packages are installed.

    **What we import and why**

    | Area | Why it matters |
    |------|----------------|
    | `pandas` | Load CSV, inspect rows, build the Excel artifact. |
    | `openpyxl` | Write `.xlsx` for submission. |
    | `openai` | Calls to the chat/completions API for generation and judging. |
    | `pydantic` | Enforce **structured** judge outputs (scores + short rationale), reducing parse errors. |

    **Secrets:** API keys live in environment variables (e.g. `OPENAI_API_KEY`), not in the notebook, so the notebook stays shareable and safe.

    > **Week 1 — context engineering:** Later, prompts will need the **right fields** in a consistent order; setup is where we commit to reading data as the single source of truth for grounding.

    > **Week 2 — evaluation-driven development:** Imports are boring on purpose: the “interesting” work is comparing runs against the **same rubric** and sample.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Phase 0: Set up your workspace once

    ### Step 1: Create a project folder

    Make one folder for the whole assignment, for example:

    ```text
    module1_LLM_Evaluation_Asignment01/
    ```

    Put inside it docs/, scripts/, data/, and models/ folders:

    * the dataset CSV in data/
    * your notebook
    * optional notes file in docs/

    ### Step 2: Create your Python environment
    ```bash
    conda create -n assignment01 python=3.11 -y
    conda activate assignment01
    conda install pandas openpyxl tqdm jupyter ipykernel nbformat -y
    pip install pydantic openai
    ```

    ### Step 3: Register the environment as a Jupyter kernel

    This is what makes your environment show up inside the notebook UI:

    ```bash
    python -m ipykernel install --user --name assignment01 --display-name "Python (assignment01)"
    ```

    ### Step 4: Open the folder

    Then open your notebook or create a new `.ipynb`.

    ### Step 5: Select the kernel

    In the notebook UI, choose:

    ```text
    Python (assignment01)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. **Inports**
    """)
    return


@app.cell
def _():
    import os
    import re
    import time
    import math
    import json
    from typing import Literal, Optional

    import pandas as pd
    from tqdm.auto import tqdm
    from pydantic import BaseModel, Field

    from openai import OpenAI

    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.Load dataset

    **Source:** CSV of products with structured columns (path relative to the notebook or a fixed `DATA_DIR`).

    - upload `data/01_agents_Assignment_01_product_dataset.csv`

    **Before any generation:**

    1. Confirm **row count** and **column names** match expectations.
    2. Spot-check a few rows for **missing values**, odd encodings, or **multi-value** fields (lists in one cell, free text in another).
    3. Note which columns are **safe to quote** verbatim vs need **paraphrase** (e.g. internal codes).

    **Grounding checklist (Week 1)**

    - Which fields are **authoritative** for factual claims (material, size, weight)?
    - Which fields are **marketing-ish** and should not be treated as independent verification?
    - Where the data is **sparse**, the model should **not** fill gaps with guesses.

    This inspection directly feeds **Task 1**: each rubric criterion should be checkable against **these** columns.

    > **Week 2 — same evaluation slice:** Keep a fixed **inspection sample** (e.g. row indices or product IDs) to reuse when comparing baseline vs improved prompts and when aligning the judge with humans.
    """)
    return


@app.cell
def _(display, pd):
    DATASET_PATH = "data/01_agents_Assignment_01_product_dataset.csv"  # change if needed

    df_products = pd.read_csv(DATASET_PATH)

    print(df_products.shape)
    print(df_products.columns.tolist())
    display(df_products.head())
    display(df_products.isna().mean().sort_values(ascending=False).head(10))
    return


@app.cell
def _(display, pd):
    DATASET_v1_PATH = "data/Assignment_01_product_dataset_CHALLENGING.csv"  # change if needed

    df_products_v1 = pd.read_csv(DATASET_v1_PATH)

    print(df_products_v1.shape)
    print(df_products_v1.columns.tolist())
    display(df_products_v1.head())
    display(df_products_v1.isna().mean().sort_values(ascending=False).head(10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dataset inspection — noise & hallucination risk (Phase 2, Step 8)

    Both course CSVs use the same schema: `product_name`, `Product_attribute_list`, `material`, `warranty`. This section records **where the data is messy** and **where a model is likely to invent or distort facts** (Week 1 **grounding**).

    #### `data/01_agents_Assignment_01_product_dataset.csv` (standard, ~50 rows)

    **Noisy fields**

    - **`Product_attribute_list`** — main source of noise: one long string mixes labeled chunks (`features:`, `dimensions:`, `rating:`, `capacity:`) with vague tags (`compact`, `large`, `sustainably sourced`, `award-winning design`, `energy efficient`, `limited edition`).
    - **Template quirks** — some rows include **`battery: long-lasting`** even for products where that label is misleading (e.g. consoles, LEGO sets, drinkware, mesh WiFi, SSDs). A model may output bogus battery-life claims.
    - **`product_name`** — relatively clean (brand + model).
    - **`material`** — short, fairly consistent.
    - **`warranty`** — varies in length and type (1-year, 2-year, lifetime, 18-month, 7-year, etc.) but usually a single phrase.

    **Hallucination hotspots**

    - Wrong or rounded **numeric specs** (MP, Hz, TB, screen size, read speeds) when paraphrasing.
    - **Ratings** (e.g. `rating: 4.7/5`) misquoted or applied to the wrong product.
    - **Vague labels** (`compact`) turned into invented sizes or weights.
    - **Features** invented when not in the string (compatibility, colors, in-box contents).
    - **Battery claims** triggered by erroneous `battery:` tails on non-battery-centric products.
    - **Warranty** shortened, genericized, or merged with a “standard” policy.

    #### `data/Assignment_01_product_dataset_CHALLENGING.csv` (~48 rows)

    **Noisy fields**

    - **`Product_attribute_list`** — dense text with **`note:`** lines: **negations** (`does NOT`), usage limits, failure modes, and timelines (e.g. “after 6 months”). Deliberate tension between shopper assumptions and what the row actually says.
    - **`warranty`** — often **multi-clause** or exclusion-heavy: tiered coverage, “normal wear,” or **no warranty** — easy to over-summarize.

    **Hallucination hotspots**

    - **Negation errors**: stating the product **does** something the attributes say it **does not** (body fat/BMI, USB-C, dishwasher-safe, local storage, heat resistance, etc.).
    - **Omitted caveats**: subscriptions, fees, filters not included, temperature ranges, return/shipping costs.
    - **Tone washing**: harsh reliability notes softened into generic marketing positives.
    - **Warranty overclaim**: broad coverage when the row excludes or limits it.
    - **Numbers and prices** (e.g. subscription fee, dB, capacities) mis-stated unless copied carefully.
    - **Prior knowledge vs row**: the model’s defaults (e.g. “smart scales measure body fat”) override explicit **`NOT`** in the data.

    #### Comparison

    | Aspect | Standard CSV | Challenging CSV |
    |--------|--------------|-----------------|
    | Main noise | Semi-structured **feature soup** + vague tags + some bogus **`battery:`** tails | Long **`note:`** blocks with **negations** and failure timelines |
    | Grounding difficulty | Keep numbers/features aligned with one messy field | Preserve **negations** and limits; avoid “helpful” corrections |
    | Warranty | Usually one line | Often **exclusions** / legal-style carve-outs |

    > **Week 2 — rubric before generation:** The challenging file is a strong stress test for rubric criteria such as **no contradictions**, **no omitted material limitations**, and **accurate warranty summary** when the assignment asks for them.

    ### Your run — fill after `head()` / missingness

    - **Rows / columns:** …
    - **Noisy or sparse fields:** …
    - **Hallucination hotspots (for the file you use):** …
    - **Fields I will treat as grounding sources:** …
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 1 — Evaluation rubric

    **Purpose:** Turn “good description” into **observable** checks so humans and (later) a judge can score consistently.

    ### Criteria (draft — refine after data inspection)

    | Criterion | Pass / scale | What “good” means | Grounding tie |
    |-----------|----------------|-------------------|---------------|
    | **Grounding** | Pass / fail or 1–5 | Claims match **only** supported attributes; no invented specs. | Hardest when attributes missing; failures = invented numbers, materials, or features. |
    | **Completeness** | … | Mentions the main customer-relevant facts present in the data. | Does not require inventing missing facts. |
    | **Clarity & tone** | … | Readable, appropriate for a product listing; no internal jargon. | Style, not truth — but must not contradict data. |
    | **Length / format** | … | Within word or bullet rules you set for the task. | Keeps cost/latency predictable (Week 1 trade-off). |

    ### Scoring rules

    - Define **pass threshold** (e.g. grounding must pass for overall pass).
    - Add **1–2 line examples** of borderline fail (e.g. “implies waterproof” when not stated).

    ### Failure buckets (Week 2)

    Use a small set of tags for manual review, e.g. `ungrounded_claim`, `missing_key_fact`, `too_vague`, `wrong_tone`, `format_violation`. These become hypotheses for prompt changes and judge prompts.

    > **Week 2 — rubric before generation:** We commit to this rubric **before** scaling generation so baseline and experiments are comparable and we avoid retro-fitting criteria to favorite outputs.

    > **Week 1 — grounding:** The rubric should make **unsupported claims** easy to mark; that is the main lever for both human eval and judge alignment later.
    """)
    return


if __name__ == "__main__":
    app.run()
