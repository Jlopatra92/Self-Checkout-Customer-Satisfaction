# Validation record

Validated locally on October 26, 2026 with Python 3.14 and the versions in `requirements-lock.txt`.

## Checks performed

- The complete polished notebook executed sequentially in a fresh Jupyter kernel with no cell errors. All 28 cells are present; 13 contain executable analysis.
- The working source workbook is copied byte-for-byte into ignored local storage; SHA-256 fingerprints match. Input fingerprint is checked again at the end of the run.
- The schema requires exactly 207 finite, complete records, the named fields, and inspected score codes. It retains the documented 5.0 speed value, duplicate profiles, and influential cases.
- The archived five-predictor regression reproduces R² rounded to 61.87% and coefficients within the source's reporting precision. Original Python mean-fold OLS/PCR2/baseline scores reproduce to three decimals in the original workbook order. Five-field K-means reproduces 163/44 clusters and silhouette about 0.398.
- All 207 records occur exactly once in each model's outer held-out evaluation. All models use the same outer split list.
- Scaling, PCA, and selected PCR component count are fitted inside training data. Component tuning uses nested inner CV. Cluster-target generation is repeated inside each outer training fold for tree evaluation.
- Full-component PCR fitted values agree with OLS within numerical tolerance.
- GroupKFold sensitivity retains all records and keeps identical predictor profiles in the same fold.
- Public notebook format and code syntax checked. No code-cell outputs or execution counts are saved in the public notebook.
- Public ZIP uses an explicit file allowlist; raw data, private results, source documents, and local paths in the private manifest are excluded.
- Notebook figure outputs inspected locally, including residual/influence diagnostics and the primary five-predictor decision tree.
- Original notebook and original workbooks fingerprinted and verified unchanged.
- Raw text responses (200+7 rows) decoded for a non-mutating aggregate lineage check: zero parsing failures and four unmatched profile occurrences on each side. No stored value changed.

## What is not validated

A fresh virtual-environment installation, other operating systems/Python versions, resolution of the four raw-to-analysis profile discrepancies, respondent independence, survey consent, and exact historical Orange evaluation settings. The original working notebook was inspected but not run wholesale because it contains exploratory errors and a package-install cell; its core methods were reproduced in the clean notebook. Dependency pins are an installed-environment snapshot, not a hash-verified cross-platform lockfile. No external cohort or causal evaluation is available.

The local Jupyter kernel required a localhost connection outside the filesystem sandbox. This was used only for execution; no remote repository or upload was performed.
