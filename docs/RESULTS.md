# Validated local findings

Run date: October 26, 2026. All values below are rounded from this project's local execution. **207 observations retained; zero deleted.** These are internal, exploratory results from encoded survey data. Public sharing of this draft and its aggregates remains subject to author review.

## Regression and uncertainty

The archived five-predictor OLS model reproduces: **in-sample R² = 0.6187; adjusted R² = 0.6092**. This is not out-of-sample performance.

| Predictor | Raw coefficient | HC3 95% interval | HC3 p-value |
|---|---:|---:|---:|
| Transaction-time field | -0.00117 | [-0.01026, 0.00791] | 0.7993 |
| Ease of use | 0.34597 | [0.17836, 0.51359] | 0.000068 |
| Technology familiarity | 0.06751 | [-0.10141, 0.23643] | 0.4316 |
| Perceived transaction speed | 0.25902 | [0.10784, 0.41020] | 0.000875 |
| Perceived security | 0.25828 | [0.15469, 0.36186] | 0.000002 |

Ease, speed, and security show positive adjusted associations in this specification. Familiarity's partial association is uncertain despite its role in segment descriptions. Coefficients are not causal effects. HC3 uses t-based intervals; p-values are exploratory and unadjusted for multiple comparisons.

Breusch–Pagan p ≈ 0.00029 and White p ≈ 0.000021 indicate heteroskedasticity concerns, supporting robust uncertainty reporting. RESET HC3 p ≈ 0.152 does not establish correct specification. Twenty-seven cases have at least one influence/leverage/residual flag; all remain. The data have 24 identical complete analysis profiles and one speed value of 5.0 that differs from the predominant midpoint coding. Neither is automatically corrected or deleted.

## Held-out prediction: identical outer folds for all models

The input now follows the original Python workbook's row order. The earlier draft used the same records in a different order, creating different seeded folds. This is a split change, not evidence that the model improved or worsened. Pooled out-of-fold scores, shuffled five-fold CV with seed 42:

| Model | RMSE | MAE | R² |
|---|---:|---:|---:|
| Training-mean baseline | 1.8720 | 1.2556 | -0.0199 |
| OLS | 1.2093 | 0.9253 | 0.5744 |
| **Two-PC PCR: primary working specification** | **1.1883** | **0.8918** | **0.5891** |
| Fixed three-PC PCR: thesis comparison | 1.1951 | 0.9031 | 0.5843 |
| PCR selected by inner 5-fold CV | 1.2316 | 0.9349 | 0.5585 |

Two-PC PCR has lower error than OLS on this fixed split scheme; the difference is not demonstrated statistically or externally. The original notebook's **mean fold** R²/MAE values also reproduce: OLS 0.559/0.926 and PCR2 0.572/0.892. Pooled R² is a different statistic from mean-fold R².

When identical predictor profiles are kept together in five GroupKFold splits, OLS pooled RMSE is **1.2000**, MAE **0.9108**, and R² **0.5809**, versus baseline RMSE **1.8559**. This is a sensitivity check, not identification of independent people. No observation is dropped.

## PCA/PCR and the thesis variance claim

Three PCs retain **84.29% of the five predictors' variance**; three-PC PCR in-sample satisfaction R² is **60.17%**. Neither supports interpreting the thesis's “over 95%” statement as satisfaction prediction performance. Archived five-predictor PCA results agree with the approximately 84.3% retention.

Six-field PCA for segmentation (age plus the five predictors) retains **63.00%** in two PCs. One separate archived PCA document includes satisfaction as a seventh input. It is documented as a historical target-inclusion risk, not evidence that every historical analysis leaked its target. The revised PCA/PCR and segmentation exclude satisfaction from PCA inputs.

## Exploratory segmentation and tree fidelity

**Primary: newer Python analysis.** K-means on five standardized predictors, without PCA or age/satisfaction inputs, reproduces clusters of **163** and **44** observations. Mean satisfaction is **8.064** and **5.136**; silhouette in that five-dimensional representation is **0.3978**. These agree with the working notebook's rounded results.

**Thesis sensitivity:** Six-field/two-PC K-means gives 164/43 observations, with mean satisfaction 8.061/5.081 and two-PC silhouette 0.4959. Its profiles match the thesis's rounded figures. This is a different representation and includes age; silhouette values across representations should not be ranked as if measuring the same geometry. The archived workbook's legacy cluster column has three groups, while the separate Orange-style export stores two.

Mean fold scores for the **primary five-field pipeline**, with scaling/K-means fitted separately on each training fold and the original tree settings (depth 5, minimum leaf 2):

| Model | Accuracy | Balanced accuracy | Macro F1 | AUC |
|---|---:|---:|---:|---:|
| Primary tree surrogate | 0.9467 | 0.9097 | 0.9180 | 0.9789 |
| Training-majority baseline | 0.7820 | 0.5000 | 0.4383 | 0.5000 |

These are cluster-fidelity scores, not accuracy for an independently observed satisfaction class. The working notebook saved 1.000 accuracy on a single 42-row holdout and mean stratified-CV accuracy 0.961, after generating labels from full-data scaling/K-means. Its upstream pipeline had already seen held-out feature values. The revised evaluation also changes the split strategy to shared outer KFold; do not attribute the score difference solely to leakage correction.

The separately labeled six-field/two-PC sensitivity uses a shallower tree (depth 3, leaf 10): mean fold accuracy 0.9177 versus majority baseline 0.7869. Its score differences combine representation and tree-setting changes. The thesis's 94.7% figure uses an incompletely documented historical pipeline and is not a direct validation benchmark.

The primary age-by-cluster chi-square statistic reproduces at approximately 7.101, with three expected counts below five. The original's saved permutation p ≈ 0.2096 does not provide strong evidence of an age association, nor prove equality of age groups; the permutation procedure was inspected but not rerun in this validation.

## Product interpretation

The findings motivate research into usability, perceived speed, and perceived security. They do not identify specific scan failures, establish that a Guided Recovery feature will work, or measure an improvement in actual checkout completion. Treat Guided Recovery as a proposed product-management learning extension. First observe the mechanism, then prototype and test with a defined comparison and eligible-session denominator.

The original Python notebook and its input are now reconciled. For author review: historical age codes, the 5.0 speed value, and four unmatched profile occurrences on each side of the raw-to-analysis multiset comparison remain unresolved. The 200+7 text responses parse successfully; their duration text specifies seconds, but does not establish instrumented timing. No case or stored value is changed to force agreement. The public notebook is output-free; detailed outputs and row diagnostics stay in ignored local storage.

Time-coding caveat: the source includes “100 seconds +”; the stored numeric value 100 represents a top-coded duration category, not a verified exact time. The source spelling “80seconds” is normalized only in the comparison parser. Analysis values are unchanged.

Author clarification (October 26, 2026): Jennifer remembers converting each rating range to its midpoint, including 7–8 → 7.5. This supports the intended coding interpretation; it does not resolve the four unmatched profile occurrences or verify every entry.
