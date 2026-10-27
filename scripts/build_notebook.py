"""Rebuild the editable, output-free public notebook from explicit cells."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
cells = []
def md(text): cells.append(nbf.v4.new_markdown_cell(text.strip()))
def code(text): cells.append(nbf.v4.new_code_cell(text.strip()))

md('''# Self-checkout customer satisfaction
### A reproducible, evidence-bounded thesis reanalysis

**Author:** Jennifer Isaac | **207 observations retained** | **Status:** local analysis; publication pending review

**Research question:** Which reported checkout attributes are associated with overall satisfaction in this sample?

Regression and PCR analyze satisfaction. PCA and K-means describe patterns; a shallow decision tree explains the resulting clusters. Neither clustering nor tree accuracy establishes an independent satisfaction prediction model.

This is a new notebook, reconciled with the author's 57-cell working notebook. The original file is preserved unchanged. The input is the working notebook's **Survey Data.xlsx**, explicitly **High Value** sheet, in its original row order. Its seven analytical fields match the archived workbook as a multiset after the documented historical age coding. Raw-response transformations remain incompletely documented. See `docs/WORKING_NOTEBOOK_REVIEW.md` for the comparison.

**Read in order:** provenance → descriptive analysis → OLS/HC3 → diagnostics → held-out prediction → PCA/PCR → segmentation/tree → thesis comparison → product hypotheses.

**Privacy:** This public notebook deliberately has no saved outputs. Running it creates a private report under ignored `outputs/`. Do not commit executed outputs, raw data, respondent plots, or row-level diagnostics without explicit permission and review.''')
md('''## 1. Reproducibility and study decisions

Seed 42; shuffled five-fold outer cross-validation shared across regression models. PCR component selection uses a separate five-fold inner CV. Scaling/PCA are fitted within training folds. No influential cases or duplicate profiles are removed. Fold variation is descriptive, not a confidence interval.

The primary regression has the five archived predictors. Age is described after the primary five-predictor clustering; only the thesis-oriented segmentation sensitivity includes age as an input. A separate age-adjusted regression sensitivity is labeled. Ratings are treated as numeric midpoint codes, an approximation to ordinal responses. Age values appear to be category representatives, not verified exact ages. Transaction time is analyzed as the stored numeric field; source response text specifies seconds. Treat it as reported duration choices, not verified instrumented timing.''')
code('''from pathlib import Path
import sys, json, platform, importlib.metadata as metadata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display, Markdown
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan, het_white, linear_reset
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score, accuracy_score, r2_score
from sklearn.model_selection import KFold, GroupKFold
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text

ROOT = Path.cwd().resolve()
if not (ROOT / 'src' / 'analysis.py').exists():
    ROOT = ROOT.parent
assert (ROOT / 'src' / 'analysis.py').exists(), 'Open from the project root or notebooks folder.'
sys.path.insert(0, str(ROOT))
from src.analysis import (SEED, PREDICTORS, SEGMENT_FEATURES, RATINGS, load_data, audit_workbook_lineage,
                          regression_cv, make_segments, tree_cv, sha256)
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'figure.figsize': (9, 5), 'axes.spines.top': False,
                     'axes.spines.right': False, 'font.size': 10})
versions = {p: metadata.version(p) for p in
            ['numpy','pandas','scipy','scikit-learn','statsmodels','matplotlib','openpyxl','nbformat','nbclient']}
display(pd.Series({'python': platform.python_version(), **versions}, name='Version').to_frame())''')
md('''## 2. Data provenance and privacy gate

Use the private copy of **Survey Data.xlsx**, **High Value** sheet (207 rows, seven fields). This is the first sheet loaded implicitly by the original notebook; it is selected explicitly here. Keep its row order so seed-42 folds reproduce the working notebook. Its other sheets include **Survey** (200 text-response rows), **New Data** (seven text-response rows), and **Median Value** (200 differently coded rows); they are not substituted. The archived **Jen survey Data 2.xlsx**, Sheet1 has the same seven-field records in a different order plus legacy PCs/clusters/silhouettes; it is a comparison source, never a source of derived predictors.

Combining the 200 and seven text-response rows and parsing their rating ranges to midpoints leaves four unmatched profile occurrences on each side of a multiset comparison with High Value. This is a coding/lineage discrepancy to resolve, not permission to alter four presumed respondents. Source time answers explicitly say “seconds,” including a top-coded “100 seconds +” category stored as 100; this supports reported duration categories, not exact instrumented timing. All stored analysis values remain unchanged.

The separate 36-response CSV archive is not the 207-row analysis dataset; it includes timestamps and survey-platform score/feedback fields. It is not merged or treated as representative raw provenance. The Orange-style export has two metadata rows preceding its 207 observations. These are format records, not cases to delete. The analysis workbook contains one speed score of 5.0 rather than a midpoint code; it is preserved exactly and flagged for author verification.

**Author clarification (October 26, 2026):** Jennifer confirmed that she remembers coding response ranges by their midpoints: 1–2 → 1.5; 3–4 → 3.5; 5–6 → 5.5; 7–8 → 7.5; 9–10 → 9.5. This is her recalled method, consistent with the predominant coding, not independent verification of every entry. The four unmatched profile occurrences and the stored 5.0 speed score remain unresolved; no values are changed.

Check `docs/DATA_PROVENANCE.md` before reuse. No obvious direct identifiers in the selected workbook does **not** mean respondent-level publication is permitted. Combinations of age and responses may still be identifying. Consent, coding, recruitment, repeated respondents, and transaction-time generation remain unresolved.''')
code('''DATA = ROOT / 'data' / 'raw' / 'survey_working_207.xlsx'
data, audit = load_data(DATA)
lineage_audit = audit_workbook_lineage(DATA)
source_hash_before = sha256(DATA)
display(pd.Series(audit, name='Audit').to_frame())
display(pd.Series(lineage_audit, name='Raw-to-analysis comparison').to_frame())
X, y = data[PREDICTORS], data.satisfaction
Z = data[SEGMENT_FEATURES]
assert len(X) == len(y) == 207
display(pd.DataFrame({'unique_values': data.nunique(), 'missing': data.isna().sum(),
                      'minimum': data.min(), 'maximum': data.max()}))
# No respondent preview is printed. No deduplication or row filtering occurs.
(OUT / 'local_audit.json').write_text(json.dumps(audit, indent=2))''')
md('''## 3. Descriptive evidence

Means summarize encoded responses; they are not behavioral measurements. Compare rating fields with each other, and keep transaction time and age on separate scales. The notebook reports duplicate profiles but retains them: identical scores do not prove duplicate people. Random-fold CV can place identical predictor profiles in different folds, so a grouped sensitivity follows.''')
code('''descriptive = data.describe().T
display(descriptive.round(3))
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
data[RATINGS].mean().sort_values().plot.barh(ax=axes[0], color='#267D91')
axes[0].set(xlim=(0,10), xlabel='Mean encoded score', title='Reported experience and satisfaction')
corr = data.corr()
im = axes[1].imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
axes[1].set_xticks(range(len(corr)), corr.columns, rotation=90)
axes[1].set_yticks(range(len(corr)), corr.columns)
axes[1].set_title('Pearson correlations: associations only')
fig.colorbar(im, ax=axes[1], shrink=.8)
plt.tight_layout(); plt.show()''')
md('''## 4. OLS with conventional and HC3 inference

OLS estimates partial associations holding the other included fields constant. HC3 changes uncertainty estimates for heteroskedasticity and leverage, not the coefficients. It does not correct confounding, measurement error, dependence, or purposive sampling. The five primary coefficient tests are exploratory, with no multiplicity adjustment; report intervals and effect sizes alongside p-values. A small p-value is not evidence of causation.

Standardized coefficients help compare scales, but are not intervention effects or a definitive product priority ranking.''')
code('''design = sm.add_constant(X)
ols = sm.OLS(y, design).fit()
hc3 = ols.get_robustcov_results(cov_type='HC3', use_t=True)
ci = hc3.conf_int()
coefficients = pd.DataFrame({
    'coefficient': ols.params, 'OLS_SE': ols.bse, 'OLS_p': ols.pvalues,
    'HC3_SE': hc3.bse, 'HC3_p': hc3.pvalues,
    'HC3_CI_low': ci[:, 0], 'HC3_CI_high': ci[:, 1],
})
standardized_beta = ols.params[PREDICTORS] * X.std(ddof=1) / y.std(ddof=1)
display(coefficients.round(5))
display(standardized_beta.rename('Standardized beta').to_frame().round(4))
display(pd.Series({'n': ols.nobs, 'R2_in_sample': ols.rsquared,
    'adjusted_R2': ols.rsquared_adj, 'residual_RMSE': np.sqrt(ols.mse_resid),
    'F_p_conventional': ols.f_pvalue}).to_frame('OLS fit'))
fig, ax = plt.subplots()
pos = np.arange(len(PREDICTORS))
c = coefficients.loc[PREDICTORS]
ax.errorbar(c.coefficient, pos,
            xerr=np.vstack([c.coefficient-c.HC3_CI_low, c.HC3_CI_high-c.coefficient]),
            fmt='o', color='#267D91', capsize=4)
ax.set_yticks(pos, PREDICTORS); ax.axvline(0, color='grey', linestyle='--')
ax.set(title='OLS coefficients with HC3 95% intervals', xlabel='Raw-scale association with satisfaction')
plt.tight_layout(); plt.show()
age_adjusted = sm.OLS(y, sm.add_constant(data[PREDICTORS + ['age']])).fit(cov_type='HC3', use_t=True)
display(pd.DataFrame({'age_adjusted_coefficient': age_adjusted.params,
                      'HC3_p': age_adjusted.pvalues}).round(5))''')
md('''## 5. Diagnostics — flag and investigate, retain every case

Residual/fitted and scale-location plots assess functional form and spread; Q-Q checks tail behavior. Breusch–Pagan and White examine heteroskedasticity; RESET checks neglected functional form; Jarque–Bera examines residual normality. These exploratory tests have their own assumptions and are not a pass/fail certificate.

Cook's distance > 4/n, leverage > 2p/n (p includes the intercept), and |externally studentized residual| > 3 are investigation flags. The private diagnostic file contains row positions for review; **no row is removed**. Row independence cannot be established from this workbook. Durbin–Watson is omitted because row order has no verified time meaning.''')
code('''influence = ols.get_influence()
cooks = influence.cooks_distance[0]
leverage = influence.hat_matrix_diag
student = influence.resid_studentized_external
n, p = design.shape
diagnostics = pd.DataFrame({'source_row_position_1based': np.arange(1,n+1),
    'cooks_distance': cooks, 'leverage': leverage, 'studentized_residual': student})
diagnostics['flag'] = (cooks > 4/n) | (leverage > 2*p/n) | (np.abs(student) > 3)
diagnostics.to_csv(OUT / 'PRIVATE_influence_diagnostics.csv', index=False)
bp = het_breuschpagan(ols.resid, design)
white = het_white(ols.resid, design)
jb = jarque_bera(ols.resid)
reset = linear_reset(ols, power=2, use_f=True, cov_type='HC3')
diagnostic_summary = {
    'Breusch_Pagan_LM_p': float(bp[1]), 'White_LM_p': float(white[1]),
    'Jarque_Bera_p': float(jb[1]), 'RESET_HC3_p': float(reset.pvalue),
    'Cook_flags': int((cooks > 4/n).sum()),
    'leverage_flags': int((leverage > 2*p/n).sum()),
    'studentized_flags': int((np.abs(student) > 3).sum()),
    'any_flag_cases_retained': int(diagnostics.flag.sum()),
    'retained_n': len(data),
}
display(pd.Series(diagnostic_summary).to_frame('Diagnostic'))
display(pd.Series({name: variance_inflation_factor(design.to_numpy(), i)
    for i, name in enumerate(design.columns) if name != 'const'}, name='VIF').to_frame())
print('Condition number after predictor standardization:',
      np.linalg.cond(sm.add_constant(StandardScaler().fit_transform(X))))
fig, axes = plt.subplots(2,2,figsize=(12,8))
axes[0,0].scatter(ols.fittedvalues, ols.resid, alpha=.6)
axes[0,0].axhline(0, color='grey'); axes[0,0].set(xlabel='Fitted', ylabel='Residual', title='Residual vs fitted')
sm.qqplot(ols.resid, line='s', ax=axes[0,1]); axes[0,1].set_title('Residual Q-Q')
axes[1,0].scatter(ols.fittedvalues, np.sqrt(np.abs(influence.resid_studentized_internal)), alpha=.6)
axes[1,0].set(xlabel='Fitted', ylabel='sqrt(|standardized residual|)', title='Scale-location')
axes[1,1].stem(np.arange(1,n+1), cooks, markerfmt=' ')
axes[1,1].axhline(4/n, color='#B54A3A', linestyle='--')
axes[1,1].set(xlabel='Private row position', ylabel="Cook's distance", title='Influence; all 207 retained')
plt.tight_layout(); plt.show()''')
md('''## 6. Five-fold predictive performance versus a mean baseline

Every respondent is held out exactly once. The baseline predicts each training fold's mean satisfaction. OLS and PCR are scored with RMSE, MAE, and R². Negative held-out R² is possible. Pooled out-of-fold R² and mean fold R² are different summaries, both labeled below.

Fixed two-component PCR preserves the working notebook's comparison; fixed three-component PCR reflects the thesis narrative. Tuned PCR chooses 1–5 components inside each training fold; its outer score includes selection. Choosing the best component count on the outer test scores would leak evaluation information. These are internal estimates, not external validation. Predictors and satisfaction were collected together, so predictive ability does not imply advance warning or a causal effect.''')
code('''splits = list(KFold(5, shuffle=True, random_state=SEED).split(X))
fold_scores, pooled_scores = regression_cv(X, y, splits)
display(fold_scores.round(4))
display(fold_scores.groupby('model')[['RMSE','MAE','R2']].agg(['mean','std']).round(4))
display(pooled_scores.round(4))
fold_scores.to_csv(OUT / 'regression_folds.csv', index=False)
pooled_scores.to_csv(OUT / 'regression_pooled_oof.csv')

# Hold identical predictor profiles together; keep all rows and test OLS vs baseline.
groups = pd.util.hash_pandas_object(X, index=False).to_numpy()
group_splits = list(GroupKFold(5).split(X, y, groups))
from sklearn.dummy import DummyRegressor
group_folds, group_pooled = regression_cv(X, y, group_splits, models={
    'Mean baseline': DummyRegressor(), 'OLS': LinearRegression()})
display(Markdown('**Sensitivity: identical predictor profiles kept in the same fold**'))
display(group_pooled.round(4))
print('Unique predictor profiles:', len(np.unique(groups)), '; rows retained:', len(data))
print('Baseline improvement, pooled OLS RMSE:',
      float(pooled_scores.loc['Mean baseline','RMSE'] - pooled_scores.loc['OLS','RMSE']))''')
md('''### Reconcile the working notebook's saved regression results

The original reports **mean fold R² and MAE**, whereas the pooled table above combines every held-out prediction. They are different statistics. The assertions below compare the same mean-fold statistic on the same workbook order, rather than treating a change in row order or summary as a method improvement.''')
code('''working_reported = pd.DataFrame({
    'model': ['Mean baseline', 'OLS', 'PCR 2 PCs (working notebook)'],
    'reported_mean_fold_R2': [np.nan, .559, .572],
    'reported_mean_fold_MAE': [1.256, .926, .892],
}).set_index('model')
working_recomputed = fold_scores.groupby('model')[['R2','MAE']].mean().rename(
    columns={'R2':'recomputed_mean_fold_R2','MAE':'recomputed_mean_fold_MAE'})
working_comparison = working_reported.join(working_recomputed)
display(working_comparison.round(3))
assert np.allclose(working_comparison.reported_mean_fold_MAE,
                   working_comparison.recomputed_mean_fold_MAE.round(3))
assert np.allclose(working_comparison.loc[['OLS','PCR 2 PCs (working notebook)'], 'reported_mean_fold_R2'],
                   working_comparison.loc[['OLS','PCR 2 PCs (working notebook)'], 'recomputed_mean_fold_R2'].round(3))''')
md('''## 7. PCA and principal component regression

PCA explains **predictor variance**, not satisfaction variance. It chooses directions without using satisfaction. A component with little predictor variance may still matter for prediction. PCR's R² and held-out error must therefore be evaluated separately.

Regression PCA uses the five archived predictors; segmentation PCA uses six fields including age. Different feature sets produce different explained-variance ratios. Signs of PCA axes are arbitrary. Five-component PCR should recover OLS fitted values (up to numerical precision) because it retains the full predictor space.''')
code('''scaler = StandardScaler().fit(X)
Xs = scaler.transform(X)
pca = PCA().fit(Xs)
pca_variance = pd.DataFrame({'PC': np.arange(1,6),
    'predictor_variance_fraction': pca.explained_variance_ratio_,
    'cumulative_predictor_variance': np.cumsum(pca.explained_variance_ratio_)})
display(pca_variance.round(4))
display(pd.DataFrame(pca.components_.T, index=PREDICTORS,
                      columns=[f'PC{i}' for i in range(1,6)]).round(4))
scores = pca.transform(Xs)
pcr3 = LinearRegression().fit(scores[:,:3], y)
pcr5 = LinearRegression().fit(scores, y)
assert np.allclose(pcr5.predict(scores), ols.fittedvalues, atol=1e-8)
back_coef = pca.components_[:3].T @ pcr3.coef_ / scaler.scale_
back_intercept = pcr3.intercept_ - back_coef @ scaler.mean_
display(pd.DataFrame({'OLS_raw_coefficient': ols.params[PREDICTORS],
                      'PCR3_backtransformed_coefficient': back_coef}).round(5))
display(pd.Series({'PCR3_in_sample_R2': r2_score(y,pcr3.predict(scores[:,:3])),
    'PCR3_predictor_variance_retained': pca.explained_variance_ratio_[:3].sum(),
    'PCR3_backtransformed_intercept': back_intercept}).to_frame('Distinct quantities'))
fig, ax = plt.subplots()
ax.bar(pca_variance.PC, pca_variance.predictor_variance_fraction, color='#267D91')
ax.plot(pca_variance.PC, pca_variance.cumulative_predictor_variance, 'o-', color='#B54A3A')
ax.set(xticks=range(1,6), xlabel='Principal component', ylabel='Fraction of predictor variance',
       title='PCA on five predictors; cumulative line is not satisfaction R²', ylim=(0,1.05))
plt.tight_layout(); plt.show()''')
md('''## 8. Primary segmentation: five standardized predictors, no PCA

The author's Python analysis uses K=2 on the full five-predictor standardized space, `n_init=20`, seed 42. Age and satisfaction are excluded; age is profiled afterward. This is the primary workflow selected by the author; the thesis-oriented six-field/two-PC analysis below is a separate sensitivity. Keep both labeled rather than silently replace the author's work. Exact profile matching does not make the clusters objectively true.

The working notebook reports an age-by-cluster permutation p-value of approximately 0.210 (10,000 permutations), and three expected chi-square cell counts below five. This is not strong evidence of an age association and does not prove age groups are equivalent. Do not apply that test to the age-inclusive clusters, which already use age to construct their labels.''')
code('''working_scaler = StandardScaler().fit(X)
working_scaled = working_scaler.transform(X)
working_kmeans = KMeans(n_clusters=2, n_init=20, random_state=SEED).fit(working_scaled)
working_labels = working_kmeans.labels_
working_profiles = data.assign(cluster=working_labels).groupby('cluster').agg(
    n=('satisfaction','size'), satisfaction_mean=('satisfaction','mean'),
    ease_mean=('ease_of_use','mean'), familiarity_mean=('technology_familiarity','mean'),
    speed_mean=('transaction_speed','mean'), security_mean=('security','mean'))
display(working_profiles.round(3))
print('Working five-field silhouette:', silhouette_score(working_scaled, working_labels))
assert sorted(working_profiles.n) == [44,163]
age_band_names = {21.0:'18-24',29.5:'25-34',39.5:'35-44',49.5:'45-54',59.5:'55-64',69.5:'65+'}
age_bands = data.age.map(age_band_names)
age_table = pd.crosstab(age_bands, working_labels)
display(age_table)
chi2, chi_p, chi_df, expected = stats.chi2_contingency(age_table)
display(pd.Series({'age_cluster_chi2':chi2, 'asymptotic_p':chi_p,
                   'expected_cells_below_5':int((expected<5).sum())}).to_frame('Working segmentation'))
assert round(float(chi2),3) == 7.101
# The thesis-oriented comparison below uses a separate, labeled specification.''')
md('''### Thesis-oriented segmentation sensitivity

Recompute standardization → PCA (two components) → K-means (K=2, 50 initializations). Age and the five experience predictors enter; satisfaction does not. The two-dimensional choice follows the thesis description, but the original Orange settings and exact preprocessing are not fully recoverable. Full-space K-means is a sensitivity. K=2 is a study choice, not proof of two natural customer populations.

Silhouette values describe separation in the fitted representation. Comparing PCA and full-space silhouettes is not a controlled performance contest. The K=2,3,4 table is descriptive, not a selection on held-out performance. Labels 0 and 1 are arbitrary. Satisfaction is summarized **after** clustering. Avoid demographic stereotypes or automatic customer targeting from these profiles.''')
code('''segmenter = make_segments(Z)
labels = segmenter.predict(Z)
embedding = segmenter[:-1].transform(Z)
profiles = data.assign(cluster=labels).groupby('cluster').agg(
    n=('satisfaction','size'), satisfaction_mean=('satisfaction','mean'),
    age_code_mean=('age','mean'), transaction_time_mean=('transaction_time','mean'),
    ease_mean=('ease_of_use','mean'), familiarity_mean=('technology_familiarity','mean'),
    speed_mean=('transaction_speed','mean'), security_mean=('security','mean'))
display(profiles.round(3))
seg_pca = segmenter.named_steps['pca']
print('Six-field PCA cumulative variance, 2 PCs:', seg_pca.explained_variance_ratio_.sum())
print('Two-PC silhouette:', silhouette_score(embedding, labels))
Zs = StandardScaler().fit_transform(Z)
full_labels = KMeans(n_clusters=2, n_init=50, random_state=SEED).fit_predict(Zs)
print('Full six-field silhouette:', silhouette_score(Zs, full_labels))
print('Two-PC vs full-space assignment agreement (ARI):', adjusted_rand_score(labels, full_labels))
sensitivity = pd.DataFrame([{'K':k, 'silhouette_2PC':silhouette_score(embedding,
    KMeans(n_clusters=k,n_init=50,random_state=SEED).fit_predict(embedding))} for k in [2,3,4]])
display(sensitivity)
fig, ax = plt.subplots()
profiles[['ease_mean','familiarity_mean','speed_mean','security_mean','satisfaction_mean']].T.plot.bar(
    ax=ax, color=['#267D91','#B54A3A'])
ax.set(ylabel='Mean encoded score', title='Exploratory cluster profiles', ylim=(0,10))
ax.tick_params(axis='x', rotation=25); plt.tight_layout(); plt.show()
# Aggregate profiles only; no individual memberships exported.
profiles.to_csv(OUT / 'cluster_profiles_aggregate.csv')''')
md('''## 9. A decision tree explaining clusters, with a majority baseline

The primary tree learns a compact approximation to the five-predictor K-means assignments using the same five inputs. A separately labeled sensitivity uses the six-field/two-PC thesis specification. High agreement can arise because both methods use the same attributes. It does not establish independent customer satisfaction prediction, validate the clusters, or justify a causal claim about technology familiarity.

For each outer fold, fit scaling and K-means **only on training rows** (the thesis sensitivity also fits PCA there); derive training labels and assign held-out rows to those fitted centroids. Fit the tree on training labels; evaluate held-out cluster-assignment agreement versus a training-majority classifier. This avoids full-dataset clustering leakage, though the target remains algorithmically constructed.

The primary tree retains the working notebook settings: maximum depth 5 and minimum leaf 2. The thesis-oriented sensitivity uses depth 3 and minimum leaf 10. These settings were not tuned on test folds; differences between the two tables combine representation and tree-setting changes. Cluster orientation uses training familiarity means, never satisfaction. Report fold accuracy, balanced accuracy, macro F1, and AUC; AUC is fidelity discrimination, not satisfaction discrimination. The final full-data tree is descriptive; its training agreement is not held-out performance.''')
code('''working_tree_scores = tree_cv(X, splits, representation='working_full5',
                                    max_depth=5, min_samples_leaf=2)
display(Markdown('**Working five-field segmentation, original tree depth/leaf settings, fold-safe labels**'))
display(working_tree_scores.groupby('model')[['accuracy','balanced_accuracy','macro_F1','AUC']].agg(['mean','std']).round(4))
tree_scores = tree_cv(Z, splits)
display(Markdown('**Thesis-oriented six-field/two-PC segmentation, shallow tree sensitivity**'))
display(tree_scores.round(4))
display(tree_scores.groupby('model')[['accuracy','balanced_accuracy','macro_F1','AUC']].agg(['mean','std']).round(4))
tree = DecisionTreeClassifier(max_depth=5, min_samples_leaf=2, random_state=SEED).fit(X, working_labels)
print('Descriptive full-data agreement:', accuracy_score(working_labels, tree.predict(X)))
print(export_text(tree, feature_names=list(X.columns)))
fig, ax = plt.subplots(figsize=(19,10))
plot_tree(tree, feature_names=list(X.columns), class_names=[f'Cluster {c}' for c in tree.classes_],
          filled=True, rounded=True, proportion=True, impurity=False, fontsize=8, ax=ax)
ax.set_title('Full-data surrogate tree: explains cluster assignments, not causal satisfaction drivers')
plt.tight_layout(); plt.show()
tree_scores.to_csv(OUT / 'tree_folds_fidelity.csv', index=False)
working_tree_scores.to_csv(OUT / 'working_tree_folds_fidelity.csv', index=False)''')
md('''## 10. Comparison with the thesis and archived analyses

The source thesis is **Jen Thesis Paper.docx**, Chapter 4; the archived numerical regression is **Regression Analysis.docx**, first five-predictor model. Existing CSV exports are useful checks but contain inconsistent specifications and formatting. They are not ground truth for revised validation.

| Source claim | Evidence boundary in this reanalysis |
|---|---|
| Five-predictor regression R² 61.87%, adjusted R² 60.92% | Test rounded reproduction below. This is in-sample fit, not 5-fold performance. |
| Ease, security, speed are prominent associations | Compare raw coefficients, standardized coefficients, HC3 intervals, and CV; do not call these intervention effects. |
| Three PCR components explain over 95% | Predictor variance and satisfaction R² are distinct. Report both calculated values; source statement is not accepted as a model validation result. |
| PCA first two PCs ≈63%, first three ≈77%, five ≈94% | Recompute with six fields including age. Thesis calls these “five variables” while listing six. |
| Archived Principal Component Analysis 2.docx | Explicitly includes Customer Satisfaction among seven PCA inputs. This is a target-inclusion risk for subsequent supervised evaluation; it does not prove the final clustering used that specification. The new PCA excludes satisfaction. |
| Two clusters with mean satisfaction 8.06 and 5.08 | Compare sorted means; do not equate label numbers across pipelines. Archived workbook actually stores C1/C2/C3. Exact cluster replication depends on original settings. |
| Tree accuracy 94.7%, reported AUC 0.927 | Original pipeline/split unknown; class AUC exports show 0.913 while average shows 0.927. Revised fold-safe fidelity is a different task evaluation. |
| Mean transaction-speed score 7.702 | Source workbook and IPA export give about 7.072; likely transposition, pending author confirmation. |
| Coefficients called standardized in narrative | Raw-scale coefficients and standardized betas differ. Archived second regression includes an unavailable “Simulated Time” field; do not conflate models. |
| Higher time implies overperformance in IPA | Time units are not comparable to rating scales, and more elapsed time is not automatically better. No mixed-unit IPA ranking is reproduced. |

No margin-of-error claim is transferred from the thesis: purposive recruitment does not justify a simple-random-sample population interval. Survey responses alone do not verify that respondents used RFID, biometric, or a specific multi-signal checkout installation.''')
code('''archive_coefficients = pd.Series([.716,-.00117,.3460,.0675,.2590,.2583], index=design.columns)
comparison = pd.DataFrame({'archived_rounded':archive_coefficients, 'recomputed':ols.params})
comparison['difference'] = comparison.recomputed - comparison.archived_rounded
display(comparison.round(7))
assert round(100*ols.rsquared,2) == 61.87
assert np.allclose(ols.params, archive_coefficients, atol=.00051)
six_pca = PCA().fit(Zs)
display(pd.Series(np.cumsum(six_pca.explained_variance_ratio_),
                  index=[f'PC1..{i}' for i in range(1,7)], name='Six-field cumulative variance').to_frame())
display(pd.DataFrame({'thesis_sorted_satisfaction_means':[5.08,8.06],
    'reanalysis_sorted_satisfaction_means':sorted(profiles.satisfaction_mean)}))
print('Verified mean transaction-speed code:', data.transaction_speed.mean())''')
md('''## 11. Product implications: evidence → hypothesis → validation

| Observed or analytical evidence | Proposed product hypothesis | Next evidence needed |
|---|---|---|
| Ease-of-use ratings have an adjusted association with satisfaction, if supported by the coefficient table | Clearer task guidance could improve experience | Observe real checkout friction; test alternative guidance against a defined comparison |
| Perceived speed and security are associated with satisfaction, if supported | Reduce verified delays and improve understandable security feedback | Logs for actual delay; comprehension and trust testing; do not equate visible reassurance with actual security |
| Exploratory profiles differ in reported familiarity and experience | Offer optional support that users can choose | Usability research across experience levels; do not assign support based on age |
| Thesis provides an academic foundation for Guided Recovery | Contextual assistance may support scan exceptions and item lookup | First establish those failures occur and matter; then prototype and test. The survey does not prove this mechanism or a solution benefit |

**Proposed validation metric:** Independent Checkout Completion Rate among predefined eligible sessions. Confirm the eligible-session denominator; handle mandatory authorizations separately. Pair completion with errors, assistance, abandonment, task time, and satisfaction. No launch, causal uplift, or improvement percentage has been demonstrated here.

**Narrative decisions for Jennifer:** Which finding is most useful to a reader, and why? Which thesis statements should be corrected versus documented as historical differences? Can you verify the coding of time/age? The author selected the newer Python analysis as the portfolio focus; thesis specifications remain comparisons. The current draft centers transparent reanalysis, not a deployed product.''')
md('''## 12. Limits, validation record, and references

Cross-sectional, purposive, self-reported data support exploratory associations within this sample. Ordinal midpoint encoding, potentially repeated respondents, ceiling effects, shared-method bias, self-reported duration choices, and incomplete raw-to-analysis lineage limit interpretation. HC3 does not resolve these issues. Fold scores on this small sample can vary with split selection. Grouping identical predictor profiles is only a sensitivity; it does not identify people or establish independence. The original working notebook is now inspected and reconciled; exact historical Orange preprocessing remains uncertain. Its exploratory Cook's-distance deletion sensitivity is documented but not carried forward: this deliverable retains every case in every full-data specification.

**Primary method documentation:**
- [scikit-learn: leakage and preprocessing pipelines](https://scikit-learn.org/stable/common_pitfalls.html)
- [statsmodels: robust covariance results](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.get_robustcov_results.html)
- [scikit-learn: PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
- [scikit-learn: KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)

Original thesis and numerical exports are private source materials listed in `docs/DATA_PROVENANCE.md`, not bundled for public distribution. See `docs/GITHUB_GUIDE.md` for review and publication steps.''')
code('''assert len(data) == 207 and not data.isna().any().any()
assert sha256(DATA) == source_hash_before, 'Input changed during analysis.'
assert sum(len(test) for _,test in splits) == 207
assert len(set(np.concatenate([test for _,test in splits]))) == 207
summary = {
    'n_retained': len(data), 'n_deleted': 0,
    'lineage_audit':lineage_audit,
    'OLS_R2_in_sample': float(ols.rsquared),
    'OLS_adjusted_R2': float(ols.rsquared_adj),
    'regression_pooled_OOF': pooled_scores.reset_index().to_dict(orient='records'),
    'grouped_profile_OOF': group_pooled.reset_index().to_dict(orient='records'),
    'PCR3_predictor_variance': float(pca.explained_variance_ratio_[:3].sum()),
    'PCR3_R2_in_sample': float(r2_score(y,pcr3.predict(scores[:,:3]))),
    'segment_2PC_variance': float(seg_pca.explained_variance_ratio_.sum()),
    'segment_silhouette': float(silhouette_score(embedding, labels)),
    'cluster_profiles': profiles.reset_index().to_dict(orient='records'),
    'working_cluster_profiles': working_profiles.reset_index().to_dict(orient='records'),
    'working_cluster_silhouette':float(silhouette_score(working_scaled,working_labels)),
    'working_tree_fidelity_fold_means':working_tree_scores.groupby('model').mean(numeric_only=True).reset_index().to_dict(orient='records'),
    'tree_fidelity_fold_means': tree_scores.groupby('model').mean(numeric_only=True).reset_index().to_dict(orient='records'),
    'diagnostics': diagnostic_summary, 'versions': versions,
}
(OUT / 'validation_summary.json').write_text(json.dumps(summary,indent=2))
display(Markdown('**Run complete:** all 207 observations retained; private input unchanged. '
                 'Outputs remain private. Review the provenance gaps before publishing any findings.'))''')
nb = nbf.v4.new_notebook(cells=cells, metadata={
    'kernelspec': {'display_name':'Python 3','language':'python','name':'python3'},
    'language_info': {'name':'python'},
    'privacy': 'Output-free public source; execution outputs must remain private.'})
nbf.validate(nb)
target = ROOT / 'notebooks' / '01_self_checkout_customer_satisfaction.ipynb'
nbf.write(nb, target)
print(f'Built {len(cells)} cells: {target.name}')
