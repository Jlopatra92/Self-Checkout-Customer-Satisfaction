# Data provenance and privacy

## Inspected source inventory

| Source | Observed contents | Use |
|---|---|---|
| Survey Data.xlsx, High Value | 207 rows, seven fields; original Python input with categorical ages | Primary analysis input; preserve original row order for seeded CV |
| Survey Data.xlsx, Survey / New Data / Median Value | 200 text-response rows / seven text-response rows / 200 alternative-coded rows | Non-mutating lineage audit; no substitution |
| Jen survey Data 2.xlsx, Sheet1 | 207 rows, 14 columns; seven source analysis fields plus PC1–PC5, Cluster, Silhouette | Archived comparison input; matching seven-field multiset with different order; derived fields excluded |
| Survey Data 3.xlsx and companion .tab | Orange-style type/role metadata rows followed by 207 records; legacy two-dimensional PCA/cluster fields | Excel's seven source fields match the primary workbook as a multiset after historical age coding, with a different row order. Stored clusters have 164/43 members; not reused as inputs |
| Survey on the Impact of Self Checkout Systems on Customer Experience form.csv.zip | One CSV with 36 responses, timestamps, platform score/feedback fields; rating ranges in answer text | Mismatched raw candidate; not merged or used for analysis |
| Jen Thesis Paper.docx | Thesis methods and Chapter 4 findings | Narrative and numerical comparison |
| Regression Analysis.docx | Five-predictor model and a second model adding “Simulated Time” | First model's coefficients and R² checked; second specification not reconstructed |
| PCA Analysis.docx | Five-predictor eigenanalysis, three PCs retain 84.3% | Agrees with recalculated predictor variance |
| Principal Component Analysis 2.docx | Seven-field eigenanalysis explicitly includes Customer Satisfaction | Historical target-inclusion risk; does not prove all historical clustering used this specification |
| IPA_Matrix_-_Regression_Based.csv; IPA_Matrix_with_PCR.csv | Means and standardized importance exports | Numerical comparison; do not accept PCR importance as proof of variance explained |
| Cluster_Interpretation_Summary.csv | Three clusters C1/C2/C3 | Evidence that source versions differ from final two-cluster thesis narrative |
| Cluster_Summary_for_Thesis_Results.csv | Classification scores, duplicate header structures, malformed `0..833` | Historical reference; not ingested as clean validation data |
| Original Python working notebook | Supplied 57-cell notebook: 56 code cells, one markdown cell; saved results and two KeyErrors | Inspected and reconciled; original left unchanged and excluded from public package |

The local manifest in ignored `outputs/PRIVATE_source_manifest.json` records source paths and SHA-256 values for the original notebook, working workbook, archived workbook, thesis, and regression document. The notebook fingerprints its private input and verifies it is unchanged during execution. No source files are edited. The local workbook is a byte-for-byte copy, not a rewritten Excel export.

## Required codebook

Whitespace is stripped from source headers, then these fields are selected:

| Source spelling | Analysis field | Interpretation and uncertainty |
|---|---|---|
| Customer Satisifaction | satisfaction | Overall satisfaction, encoded 1.5/3.5/5.5/7.5/9.5 |
| Transaction Time | transaction_time | Numeric field, observed range 40–100. Source text responses specify seconds; treat as reported duration choices, not instrumented timing |
| Ease of Use | ease_of_use | Encoded experience rating |
| Technology familarity | technology_familiarity | Encoded familiarity/comfort rating |
| Transaction speed | transaction_speed | Encoded perceived-speed rating; distinct from numeric time |
| Security | security | Encoded perceived security, not measured security effectiveness |
| Age | age | Original categories preserved as the interpretation. Historical numeric codes: 18–24→21; 25–34→29.5; 35–44→39.5; 45–54→49.5; 55–64→59.5; 65+→69.5. The final open-ended category has no mathematical midpoint; its numeric representative is a legacy convention |

The original workbook now supplies 200+7 text-response rows. Parsing duration strings as seconds and rating ranges as midpoints yields zero parsing failures, but four unmatched profile occurrences on each side of a multiset comparison with High Value. This does not identify four particular people or establish which coding is correct. The separate 36-response CSV is still not a substitute. One transaction-speed value is 5.0 rather than a midpoint code; it is retained verbatim, not recoded or deleted. Do not claim an audited raw-to-analysis transformation. Ask the author to verify all coding, including this anomaly, reverse coding, and age-category handling.

## Privacy observations

- The seven selected analysis fields and inspected response-sheet schemas contain no obvious names, emails, phone numbers, addresses, respondent IDs, or timestamps. The archived comparison workbook's extra fields are legacy analytical outputs; the working workbook's other sheets contain earlier text/alternative-coded responses.
- This is a schema/content observation, not an anonymization certification. Numeric age and unusual response combinations may permit reidentification.
- The CSV archive includes timestamps and has a different cohort size; its timing/source is not consistent enough to reconcile with the thesis collection description without author input.
- No direct or derived respondent records are published. Raw workbooks, `.tab` exports, source documents, row diagnostics, fitted plots, and executed notebooks stay private.
- `.gitignore` reduces accidental staging but does not remove previously tracked files or sanitize outputs. The public archive uses an explicit allowlist. The checker is a narrow technical gate, not a complete privacy audit.

## Open questions before stronger claims

1. Resolve the four unmatched raw/analysis profile occurrences on each side of the lineage comparison. The original notebook and working source workbook are now located and reconciled; which coding/source version should be authoritative?
2. What recruitment, consent, institutional approval, and sharing terms apply? Does consent cover public secondary analysis or even publication of aggregates?
3. The source response sheets specify durations in seconds. Confirm whether these were selected reported categories and how values were encoded; they are not verified system logs. The regression archive includes an additional simulated-time model whose field is absent from this workbook.
4. How were age and rating bands encoded? Are there repeated respondents, household/site clusters, or resubmissions?
5. What were the final Orange PCA/scaling/K-means settings and Test & Score folds? The 207-row workbook retains three legacy clusters; final thesis describes two.
6. Did participants use ordinary self-checkout or verified multi-signal checkout technology? The survey question text alone does not establish specific hardware exposure.

All 207 rows remain in every full-data model. All 207 receive held-out evaluation across outer folds. Identical profiles and influential observations are retained and documented.

Time-coding caveat: the source includes “100 seconds +”; the stored numeric value 100 represents a top-coded duration category, not a verified exact time. The source spelling “80seconds” is normalized only in the comparison parser. Analysis values are unchanged.

## Author clarification: midpoint coding

On October 26, 2026, Jennifer confirmed that she remembers converting response ranges using their midpoints: 1–2 → 1.5; 3–4 → 3.5; 5–6 → 5.5; 7–8 → 7.5; 9–10 → 9.5. This is the author's recalled preparation method, consistent with the predominant workbook coding, rather than an independently verified record of every transformation. It does not resolve the four unmatched profile occurrences on each side of the raw-to-analysis comparison or the stored speed score of 5.0. No data value was changed.
