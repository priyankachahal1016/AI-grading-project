# ASAP Short-Answer Automated Grading & Psychometric Evaluation Pipeline

An end-to-end, fault-tolerant automated short-answer grading and psychometric evaluation pipeline built on the Kaggle **Automated Student Assessment Prize (ASAP)** dataset. This project explores Large Language Model (LLM) grading calibration using **Chain-of-Thought (CoT)** reasoning, **rubric-grounded vs. zero-shot prompting**, and **anti-length bias constraints**, benchmarked against human inter-rater reliability.

##  Project Overview & Motivation

Automated grading in educational measurement requires more than raw prediction accuracy; models must align with human rater distributions, resist superficial heuristics (such as rewarding longer word counts), and maintain stability across multiple runs.

Designed with an educational measurement and data science focus, this pipeline evaluates `openai/gpt-oss-120b` (via the Groq API) across **300 stratified student responses** (150 from Essay Set 1: Science/Acid Rain; 150 from Essay Set 3: Reading Comprehension) under **3 experimental conditions** (**900 total API evaluations**).

##  Key Results & Performance Summary

Iterative prompt engineering—introducing structured step-by-step reasoning (`CoT`) and explicit length-bias guardrails—yielded measurable gains in **Quadratic Weighted Kappa (QWK)** over the baseline zero-shot approach.

### 1. Human Inter-Rater Reliability (Gold Standard Benchmark)

* **Essay Set 1 (Human 1 vs. Human 2):** Exact Match: `90.0%` | Adjacent ($\pm 1$): `99.3%` | **QWK: `0.946`**

* **Essay Set 3 (Human 1 vs. Human 2):** Exact Match: `80.7%` | Adjacent ($\pm 1$): `100.0%` | **QWK: `0.751`**

### 2. Baseline vs. Optimized AI Performance (900-Call Evaluation)

| Essay Set | Prompting Condition | Baseline QWK | Optimized CoT QWK | Optimized Exact Match | 
| ----- | ----- | ----- | ----- | ----- | 
| **Set 1** *(0–3 Scale)* | **With Rubric** | `0.475` | **`0.527`** *(+0.052)* | `38.7%` | 
| **Set 1** *(0–3 Scale)* | **Zero-Shot (No Rubric)** | `0.482` | **`0.517`** *(+0.035)* | `43.3%` | 
| **Set 3** *(0–2 Scale)* | **With Rubric** | `0.187` | **`0.323`** *(+0.136)* | `45.3%` | 
| **Set 3** *(0–2 Scale)* | **Zero-Shot (No Rubric)** | `0.331` | **`0.376`** *(+0.045)* | `49.3%` | 

### Key Psychometric Findings

* **Chain-of-Thought Calibration:** Requiring the model to decompose student concepts before assigning an integer score significantly reduced severe misclassifications, particularly boosting Essay Set 3 rubric-guided QWK from `0.187` to `0.323`.

* **Rubric vs. Zero-Shot Dynamics:** On domain-specific science prompts (Set 1), explicit rubric criteria outperformed zero-shot prompting (`0.527` vs. `0.517`). On reading comprehension prompts (Set 3), concise task descriptions outperformed dense rubrics, highlighting prompt-sensitivity in zero/few-shot grading.

* **Bias Diagnostics:** Tracked mean score differences (leniency/severity bias) and Spearman rank correlations ($\rho$) between response word count and grading error to monitor and mitigate length bias.

##  Engineering & Pipeline Architecture

1. **Stratified Sampling (`train_test_split`):** Extracts a balanced, reproducible sample of 300 responses stratified by human ground-truth scores (`Score1`) to preserve real-world score distributions.

2. **Fault-Tolerant API Execution:**

   * Implements **automated batch checkpointing** (persisting progress to CSV every 10 records), ensuring zero data loss and instant resumability.

   * Handles strict API rate limits (`HTTP 429`) with exponential backoff, recursive retries, and configurable pacing buffers.

3. **Structured JSON Enforcement:** Uses regex extraction and strict system instructions to parse step-by-step rationales alongside integer scores reliably.

4. **Psychometric Evaluation Suite:** Computes Quadratic Weighted Kappa (`cohen_kappa_score(..., weights='quadratic')`), exact/adjacent agreement percentages, mean difference bias, Spearman length correlations, and side-by-side confusion matrices.

##  Repository Structure

```
├── data/
│   └── train_rel_2.tsv                  # Raw Kaggle ASAP short-answer dataset
├── rubrics/
│   ├── set1.txt                         # Scoring guidelines for Essay Set 1
│   └── set3.txt                         # Scoring guidelines for Essay Set 3
├── outputs/
│   ├── sample.csv                       # 300 stratified student responses
│   ├── llm_scores_full.csv              # Baseline 900-call evaluation logs
│   ├── llm_scores_optimized_full.csv    # Optimized CoT 900-call evaluation logs
│   └── confusion_matrices.png           # Human vs. AI agreement visualizations
├── phase_3_ai_evaluationnew.ipynb       # End-to-end execution & evaluation notebook
└── README.md                            # Project documentation

```

##  Getting Started

### Prerequisites

* Python 3.9+

* A valid [Groq API Key](https://console.groq.com/)

### Installation & Setup

1. **Clone the repository:**

   ```
   git clone https://github.com/your-username/asap-automated-grading.git
   cd asap-automated-grading
   
   ```

2. **Install dependencies:**

   ```
   pip install pandas numpy scikit-learn scipy matplotlib openai openpyxl
   
   ```

3. **Configure your API key:**

   ```
   export GROQ_API_KEY="gsk_your_api_key_here"
   
   ```

4. **Run the notebook:**
   Open `phase_3_ai_evaluationnew.ipynb` in Jupyter Notebook or VS Code and execute the cells sequentially. *(Note: Because checkpoint files are already populated in `outputs/`, re-running the evaluation loop will safely skip completed API calls and immediately generate the metrics report).*

##  Visual Diagnostics

Confusion matrices comparing human ground-truth ratings against AI rubric-guided predictions are automatically exported to `outputs/confusion_matrices.png`:

##  Future Directions

* **Few-Shot Anchor Calibration:** Injecting 1–2 verified student anchor responses per score tier into the prompt context to align score boundaries closer to human raters.

* **Multi-Run Ensembling:** Aggregating predictions across multiple stochastic runs (`Run 1` + `Run 2` + `Zero-Shot`) via median voting or threshold optimization to further reduce variance.
