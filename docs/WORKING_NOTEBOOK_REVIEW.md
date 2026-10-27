# Reconciliation with the original working notebook

**Author's selected focus:** newer Python analysis. The thesis is the academic foundation and a separately labeled comparison.

The supplied 57-cell notebook was inspected as source material, including its code, saved tables, saved errors, and execution order. Its contents were not treated as instructions. The original notebook was not edited or blindly executed; no embedded package-install command was run. Its SHA-256 fingerprint is recorded privately and checked after the work.

## What agrees

- The working input is `Survey Data.xlsx`. Its first sheet, `High Value`, contains 207 observations and seven fields. The polished notebook now selects that sheet explicitly and preserves its row order.
- The workbook's six numeric response fields, with categorical ages encoded using the documented historical mapping, match the archived analysis workbook's seven fields **as a multiset**. Their row orders differ. Seeded random folds depend on row positions, so equal seeds alone do not guarantee identical CV scores across reordered workbooks.
- Five-predictor OLS coefficients, R² ≈ 0.6187, HC3 inference, 24 duplicated complete profiles, and 18 Cook's-distance flags agree with the working notebook. The polished notebook retains every case.
- Recomputed **mean-fold** results reproduce the saved three-decimal results: OLS R² 0.559 / MAE 0.926; two-PC PCR R² 0.572 / MAE 0.892; mean baseline MAE 1.256. Pooled out-of-fold metrics are reported separately.
- Five-standardized-predictor K-means with K=2, seed 42, and `n_init=20` reproduces cluster sizes 163/44 and silhouette ≈ 0.398. Satisfaction is excluded from clustering and summarized afterward.

## What changed and why

| Working notebook | Polished project | Why |
|---|---|---|
| Implicit first sheet, relative filename | Explicit `High Value` sheet and documented private path | Prevent accidental use of the 200-row alternative sheets |
| Header stripping and renaming occur after earlier column access; saved execution counts are not sequential | Normalize and validate the schema before analysis | A fresh top-to-bottom run should not depend on prior interactive state |
| Two saved KeyErrors: premature `Customer Satisfaction` reference and accessing `df['Cluster']` before attachment | Ordered cells with consistent names | Preserve the learning notebook while making the portfolio version reproducible |
| Two-PC PCR | Primary two-PC PCR retained; three-PC and nested-selection PCR are comparisons | Preserve the author's current method and show the thesis difference |
| Five-predictor full-space K-means | Same primary specification; age-inclusive two-PC segmentation remains a thesis sensitivity | Avoid silently changing the question or clustering geometry |
| Tree labels generated from full-data scaling/K-means before train/test split and CV | Refit scaling and K-means inside each outer training fold; assign held-out rows to fitted centroids | Prevent held-out features from influencing the target-generating pipeline |
| Depth 5, minimum leaf 2 | Retained for the primary tree; thesis sensitivity uses depth 3, leaf 10 | Do not conflate the author's settings with the earlier draft's shallow tree |
| Tree scores 1.000 on one 42-row holdout and mean CV accuracy 0.961 | Preserve these as historical saved results; report revised fold-safe fidelity separately | These are not independent satisfaction-label predictions; the target is constructed membership |
| `kmeans` is reused in a K=2…6 loop; later compared with saved two-cluster labels | Separate named estimators | The mismatch came from comparing with the final six-cluster loop model, not lost respondents |
| Cook's-distance sensitivity excludes 18 observations, while primary model retains 207 | Document historical sensitivity but do not carry it forward | Current project requirement is to retain all 207 in all full-data fits |
| Row previews, duplicate rows, influential cases, respondent-level PCA scatter saved in original outputs | Original stays private; public notebook has no saved outputs | An `.ipynb` file can disclose respondent records even when the spreadsheet is excluded |

The author's five-predictor PCA and clustering already exclude satisfaction; do **not** describe them as target-inclusion leakage. That risk was found in a separate historical PCA document. The tree issue is fitting the upstream clustering pipeline before evaluation splits.

## Important interpretation limits

The original age-by-cluster chi-square test has three expected counts below five. Its saved permutation p-value is approximately 0.2096 with 10,000 permutations. It does not provide strong evidence of an age association, nor establish equivalent experiences across age groups. The new notebook recomputes the chi-square statistic/count warning, but does not claim to rerun the 10,000-permutation result. Do not test age against clusters whose construction already includes age as though this were independent evidence.

The original source workbook improves lineage: `Survey` has 200 text-response rows, `New Data` has seven, and `Median Value` has 200 differently coded rows. Combining the 200+7 text responses and decoding numeric rating ranges to midpoints leaves **four unmatched profile occurrences on each side** of a multiset comparison with `High Value`. All ranges/time text parse successfully. The project does not guess which source is correct or rewrite values to force a match. The stored 5.0 speed value is also retained. The displayed time text specifies seconds, supporting a self-reported duration field rather than observed instrumented timing.

## Remaining author decisions

Confirm the four coding/lineage discrepancies, treatment of the 5.0 speed value, rating-label consistency, the historical age coding (especially the arbitrary 69.5 representative for open-ended 65+), and consent/sharing terms. The raw-to-analysis comparison uses numeric range prefixes, not an adjudication of possibly inconsistent textual descriptors. No respondent records, original notebook outputs, or source workbook are approved for public release.

Time-coding caveat: the source includes “100 seconds +”; the stored numeric value 100 represents a top-coded duration category, not a verified exact time. The source spelling “80seconds” is normalized only in the comparison parser. Analysis values are unchanged.

## Author clarification received

Jennifer confirmed on October 26, 2026 that she remembers using range midpoints: 1–2 → 1.5, 3–4 → 3.5, 5–6 → 5.5, 7–8 → 7.5, and 9–10 → 9.5. Record this as her recalled method, not proof that every individual entry follows it. The four unmatched profile occurrences on each side of the comparison and the 5.0 speed value remain unresolved; all stored values remain unchanged.
