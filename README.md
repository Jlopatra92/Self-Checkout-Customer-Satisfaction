# Self-Checkout Customer Satisfaction: Thesis Reanalysis

**What drives customer satisfaction at self-checkout, and what should a product team do about it?**

I rebuilt my master's thesis analysis (originally in Excel, SPSS, and Orange) as reproducible
Python code to test whether the original findings hold up under stricter validation, then used
the results to frame a product hypothesis.

## Key findings
- **Perceived** ease of use, speed, and security had the strongest positive associations with satisfaction.
- **Self-reported transaction time did not.** How fast checkout felt mattered more than how long people said it took.
- Two customer segments emerged: 163 respondents averaging 8.1/10 satisfaction, and 44 averaging 5.1/10.
- On held-out data, the model explains roughly 57–59% of the variation in satisfaction (5-fold cross-validation).

## From findings to product
These results point to friction in the checkout experience, not raw speed. I translated them into a
PRD for **Guided Recovery**, a proposed feature that [ONE LINE: what it does for the customer].
→ **[Read the PRD]([NETLIFY LINK])**

These are survey associations, not causal effects. The PRD treats Guided Recovery as a hypothesis to test.
## What the reanalysis showed
This project tested the stability of my thesis conclusions through reproducible validation.
The main relationships held: perceived ease of use, speed, and security remain the strongest
drivers of satisfaction. The predictive and causal claims need to be stated more modestly.
- Full comparison: [docs/RESULTS.md](docs/RESULTS.md)

## Data and privacy
Code and aggregate findings are public. Respondent-level survey data are excluded and are not
redistributed; access is subject to participant consent and institutional terms.

Private repository: [Jlopatra92/self-checkout-customer-satisfaction](https://github.com/Jlopatra92/self-checkout-customer-satisfaction).

## Start here

- [Polished notebook](notebooks/01_self_checkout_customer_satisfaction.ipynb)
- [Results and thesis differences](docs/RESULTS.md)
- [Original working notebook comparison](docs/WORKING_NOTEBOOK_REVIEW.md)
- [Data provenance and privacy](docs/DATA_PROVENANCE.md)
- [Validation record](docs/VALIDATION.md)
- [Narrative decisions for Jennifer](docs/NARRATIVE_REVIEW.md)
- [Step-by-step GitHub guide](docs/GITHUB_GUIDE.md)

## What the project contains

1. Explicit schema, source fingerprint, missingness, coding, and duplicate-profile checks.
2. Five-predictor OLS, conventional and HC3 uncertainty, standardized coefficients, and age-adjusted sensitivity.
3. Residual/Q-Q/influence plots, heteroskedasticity tests, functional-form check, VIF, and investigation flags. No cases deleted.
4. Shared five-fold CV: mean baseline, OLS, primary fixed two-PC PCR, three-PC thesis comparison, and nested component-selection PCR. RMSE, MAE, and R²; grouped-profile sensitivity for OLS/baseline.
5. PCA variance/loadings, PCR back-transformed coefficients, and full-component PCR/OLS equivalence check.
6. Primary five-predictor, full-space, two-cluster K-means; a separate six-field/two-PC thesis sensitivity.
7. Fold-specific clustering and a tree surrogate versus majority baseline; accuracy, balanced accuracy, macro F1, and AUC quantify cluster fidelity.
8. Thesis comparisons, methodological caveats, and proposed product hypotheses with validation needs.

## Run locally

The validated environment is Python 3.14. Dependency pins reflect the installed environment; other Python versions and a fresh installation have not been tested. `requirements.txt` pins direct dependencies, while `requirements-lock.txt` records the resolved dependency closure from the validated environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m ipykernel install --sys-prefix --name python3 --display-name 'Self-checkout project'
```

Place the privately authorized **Survey Data.xlsx** workbook at `data/raw/survey_working_207.xlsx`. Keep its High Value, Survey, and New Data sheets and source column names unchanged. The notebook analyzes High Value and audits the text-response sheets without replacing the analysis values. A local ignored copy is already present in the author's workspace; the public package deliberately excludes it. See the provenance document for the required schema. Without authorized data, readers can inspect code and the documented aggregate findings but cannot reproduce the empirical results. No synthetic data is passed off as thesis data.

From the project root:

```bash
python scripts/run_notebook.py
python scripts/check_public.py
jupyter lab notebooks/01_self_checkout_customer_satisfaction.ipynb
```

The execution script saves the private result to `outputs/PRIVATE_self_checkout.executed.ipynb` and leaves the source notebook output-free. Opening and running the public notebook interactively can save private results into it: clear all outputs before staging, and rerun the public checker. To regenerate the clean notebook from its cell source:

```bash
python scripts/build_notebook.py
```

## Structure

```text
notebooks/  polished, editable notebook with no saved outputs
src/        explicit schema and reusable modeling helpers
scripts/    rebuild, execute, and prepublication checks
docs/       provenance, results, validation, author review, GitHub steps
data/raw/   ignored private analysis input
outputs/    ignored execution results and private diagnostics
```

## Interpretation and access

PCA predictor variance is not the satisfaction-model R². The tree predicts constructed cluster membership, not independently observed satisfaction. Same-survey associations cannot establish what an intervention would change. Midpoint coding, purposive sampling, four unmatched raw/analysis profile occurrences on each side of the lineage check, and self-reported time measurement limit conclusions. Do not infer actual checkout technology adoption from the thesis title.

No respondent-level data, private source documents, executed notebook, or local diagnostic plots are included in the public package. No redistribution permission or open-data license is implied. Contact the author to discuss permitted access; data sharing remains subject to consent and institutional requirements.

Primary implementation references: [scikit-learn leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html) and [statsmodels robust covariance documentation](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.get_robustcov_results.html).
