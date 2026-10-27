# Self-checkout customer satisfaction

Jennifer Isaac's reproducible thesis reanalysis: **207 observations, all retained**. OLS and principal component regression analyze associations with satisfaction. PCA/K-means explore customer profiles; a shallow decision tree explains algorithmic cluster assignments.

**Status:** validated research project; the author approved a private GitHub repository. Public release and respondent-level data sharing remain unapproved. This is an exploratory academic portfolio project, not a deployed product or causal impact study. The original Python notebook has now been inspected and preserved unchanged. The author selected the newer Python analysis as the portfolio focus. Results use its original workbook and row order; thesis specifications remain clearly labeled comparisons.

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

Place the privately authorized **Survey Data.xlsx** workbook at `data/raw/survey_working_207.xlsx`. Keep its High Value, Survey, and New Data sheets and source column names unchanged. The notebook analyzes High Value and audits the text-response sheets without replacing the analysis values. A local ignored copy is already present in the author's workspace; the public package deliberately excludes it. See the provenance document for the required schema. Without authorized data, readers can inspect code and the documented aggregate findings but cannot reproduce the empirical results. No synthetic data are passed off as thesis data.

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

PCA predictor variance is not satisfaction-model R². The tree predicts constructed cluster membership, not independently observed satisfaction. Same-survey associations cannot establish what an intervention would change. Midpoint coding, purposive sampling, four unmatched raw/analysis profile occurrences on each side of the lineage check, and self-reported time measurement limit conclusions. Do not infer actual checkout technology adoption from the thesis title.

No respondent-level data, private source documents, executed notebook, or local diagnostic plots are included in the public package. No redistribution permission or open-data license is implied. Contact the author to discuss permitted access; data sharing remains subject to consent and institutional requirements.

Primary implementation references: [scikit-learn leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html) and [statsmodels robust covariance documentation](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.get_robustcov_results.html).
