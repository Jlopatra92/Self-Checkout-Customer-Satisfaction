"""Explicit schema, fold-safe modeling, and aggregate-only reporting helpers.

No source notebook is imported or edited. All rows are retained.
"""
from pathlib import Path
import hashlib
import re
from collections import Counter
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, f1_score,
                             mean_absolute_error, mean_squared_error, r2_score,
                             roc_auc_score)
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

SEED = 42
RENAME = {
    'Customer Satisifaction': 'satisfaction', 'Age': 'age',
    'Transaction Time': 'transaction_time', 'Ease of Use': 'ease_of_use',
    'Technology familarity': 'technology_familiarity',
    'Transaction speed': 'transaction_speed', 'Security': 'security',
}
PREDICTORS = ['transaction_time', 'ease_of_use', 'technology_familiarity',
              'transaction_speed', 'security']
SEGMENT_FEATURES = ['age'] + PREDICTORS
RATINGS = ['satisfaction', 'ease_of_use', 'technology_familiarity',
           'transaction_speed', 'security']

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def audit_workbook_lineage(path):
    """Compare stored analysis records with range-midpoint decoding, without edits.

    This is an aggregate multiset check, not respondent identity matching.
    """
    high = pd.read_excel(path, sheet_name='High Value')
    survey = pd.read_excel(path, sheet_name='Survey')
    extra = pd.read_excel(path, sheet_name='New Data')
    for frame in [high, survey, extra]: frame.columns = frame.columns.str.strip()
    extra = extra.rename(columns={'Easy of Use':'Ease of Use',
        'Technology Familarity':'Technology familarity', 'Transaction Speed':'Transaction speed',
        'Customer satisfaction':'Customer Satisifaction'})
    columns = list(high.columns)
    raw = pd.concat([survey[columns], extra[columns]], ignore_index=True)
    decoded = raw.copy()
    for col in columns:
        if col == 'Age': continue
        def decode(value):
            text = str(value).strip()
            if col == 'Transaction Time':
                # Source spelling includes '80seconds' and top-coded '100 seconds +'.
                match = re.match(r'^(\d+)\s*seconds?\s*\+?\s*$', text, flags=re.I)
                return float(match[1]) if match else np.nan
            match = re.match(r'^(\d+)\s*[-–]\s*(\d+)', text)
            return (int(match[1]) + int(match[2])) / 2 if match else np.nan
        decoded[col] = decoded[col].map(decode)
    stored = Counter(map(tuple, high[columns].to_numpy()))
    reconstructed = Counter(map(tuple, decoded[columns].to_numpy()))
    return {'raw_text_survey_rows':len(survey), 'additional_text_rows':len(extra),
            'combined_text_rows':len(raw), 'unparsed_values':int(decoded.isna().sum().sum()),
            'top_coded_100plus_duration_responses':int(raw['Transaction Time'].astype(str).str.contains(r'\+',regex=True).sum()),
            'unmatched_analysis_profile_occurrences':sum((stored-reconstructed).values()),
            'unmatched_reconstructed_profile_occurrences':sum((reconstructed-stored).values()),
            'policy':'Preserve stored 207-row analysis; author must resolve coding differences.'}

def load_data(path, sheet_name='High Value'):
    """Fail on schema drift, missingness, or unexpected scores; never drop rows."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f'Private data missing: {path.name}. See docs/DATA_PROVENANCE.md; '
            'the public project intentionally contains no respondent data.')
    raw = pd.read_excel(path, sheet_name=sheet_name)
    raw.columns = raw.columns.str.strip()
    if raw.columns.duplicated().any():
        raise ValueError('Duplicate column names after whitespace normalization.')
    missing = set(RENAME) - set(raw.columns)
    if missing:
        raise ValueError(f'Unrecognized source schema; missing {sorted(missing)}')
    # Explicit allowlist excludes legacy PCs, cluster IDs, silhouettes and identifiers.
    data = raw[list(RENAME)].rename(columns=RENAME)
    if not pd.api.types.is_numeric_dtype(data.age):
        age_codes = {'18-24':21, '25-34':29.5, '35-44':39.5,
                     '45-54':49.5, '55-64':59.5, '65+':69.5}
        if not data.age.isin(age_codes).all():
            raise ValueError('Unrecognized age band; do not silently encode.')
        data.age = data.age.map(age_codes)
    data = data.apply(pd.to_numeric, errors='raise')
    if len(data) != 207 or data.isna().any().any() or not np.isfinite(data).all().all():
        raise ValueError('Expected exactly 207 finite, complete rows. Investigate; do not delete.')
    midpoint_codes = [1.5, 3.5, 5.5, 7.5, 9.5]
    for column in RATINGS:
        # The inspected source has one non-midpoint speed value (5.0).
        # Preserve it verbatim and disclose it; never silently recode the source.
        allowed = midpoint_codes + ([5.0] if column == 'transaction_speed' else [])
        if not data[column].isin(allowed).all():
            raise ValueError(f'Unexpected rating code in {column}; verify codebook.')
    if not (data.age.gt(0).all() and data.transaction_time.gt(0).all()):
        raise ValueError('Unexpected nonpositive age/time code.')
    audit = {
        'file_sha256': sha256(path), 'rows': len(data), 'source_columns': len(raw.columns),
        'sheet': sheet_name,
        'analysis_columns': len(data.columns), 'missing_cells': int(data.isna().sum().sum()),
        'identical_analysis_rows_retained': int(data.duplicated().sum()),
        'non_midpoint_speed_values_retained': int((data.transaction_speed == 5.0).sum()),
        'excluded_columns': [c for c in raw.columns if c not in RENAME],
        'privacy_status': 'No obvious direct identifiers in selected fields; NOT clearance for publication.',
    }
    return data, audit

def regression_models():
    return {
        'Mean baseline': DummyRegressor(strategy='mean'),
        'OLS': LinearRegression(),
        'PCR 2 PCs (working notebook)': Pipeline([
            ('scale', StandardScaler()), ('pca', PCA(n_components=2)),
            ('regression', LinearRegression())]),
        'PCR 3 PCs (fixed)': Pipeline([
            ('scale', StandardScaler()), ('pca', PCA(n_components=3)),
            ('regression', LinearRegression())]),
        'PCR (inner-CV selected)': GridSearchCV(
            Pipeline([('scale', StandardScaler()), ('pca', PCA()),
                      ('regression', LinearRegression())]),
            {'pca__n_components': [1, 2, 3, 4, 5]},
            scoring='neg_mean_squared_error',
            cv=KFold(5, shuffle=True, random_state=SEED + 1), n_jobs=1),
    }

def regression_cv(X, y, splits, models=None):
    """Return fold metrics and pooled out-of-fold metrics on identical splits."""
    models = regression_models() if models is None else models
    folds, pooled = [], []
    for name, estimator in models.items():
        oof = np.full(len(y), np.nan)
        for fold, (train, test) in enumerate(splits, 1):
            fit = clone(estimator).fit(X.iloc[train], y.iloc[train])
            prediction = fit.predict(X.iloc[test])
            oof[test] = prediction
            folds.append(dict(model=name, fold=fold, n_test=len(test),
                RMSE=float(np.sqrt(mean_squared_error(y.iloc[test], prediction))),
                MAE=mean_absolute_error(y.iloc[test], prediction),
                R2=r2_score(y.iloc[test], prediction),
                selected_PCs=(fit.best_params_['pca__n_components']
                              if isinstance(fit, GridSearchCV) else np.nan)))
        assert np.isfinite(oof).all()
        pooled.append(dict(model=name, RMSE=float(np.sqrt(mean_squared_error(y, oof))),
                           MAE=mean_absolute_error(y, oof), R2=r2_score(y, oof)))
    return pd.DataFrame(folds), pd.DataFrame(pooled).set_index('model')

def make_segments(X):
    """Six standardized fields -> two PCs -> K=2. Satisfaction never enters."""
    pipeline = Pipeline([('scale', StandardScaler()), ('pca', PCA(n_components=2)),
                         ('kmeans', KMeans(n_clusters=2, n_init=50, random_state=SEED))])
    pipeline.fit(X)
    return pipeline

def tree_cv(X, splits, representation='thesis_pca2', max_depth=3, min_samples_leaf=10):
    """Assess surrogate fidelity to TRAINING-ONLY clusters, not satisfaction."""
    rows = []
    for fold, (train, test) in enumerate(splits, 1):
        Xtrain, Xtest = X.iloc[train], X.iloc[test]
        if representation == 'working_full5':
            segmenter = Pipeline([('scale', StandardScaler()), ('kmeans', KMeans(
                n_clusters=2, n_init=20, random_state=SEED))]).fit(Xtrain)
        elif representation == 'thesis_pca2':
            segmenter = make_segments(Xtrain)
        else:
            raise ValueError('Unknown cluster representation')
        train_labels = segmenter.predict(Xtrain)
        test_labels = segmenter.predict(Xtest)
        # Relabel using training feature means only; no satisfaction-based naming.
        mean_familiarity = Xtrain.groupby(train_labels).technology_familiarity.mean()
        positive = mean_familiarity.idxmax()
        ytrain = (train_labels == positive).astype(int)
        ytest = (test_labels == positive).astype(int)
        for name, model in {
            f'Tree (depth {max_depth}, leaf {min_samples_leaf})': DecisionTreeClassifier(
                max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=SEED),
            'Majority baseline': DummyClassifier(strategy='most_frequent'),
        }.items():
            model.fit(Xtrain, ytrain)
            pred = model.predict(Xtest)
            prob = model.predict_proba(Xtest)[:, list(model.classes_).index(1)]
            rows.append(dict(model=name, fold=fold, n_test=len(test),
                accuracy=accuracy_score(ytest, pred),
                balanced_accuracy=balanced_accuracy_score(ytest, pred),
                macro_F1=f1_score(ytest, pred, average='macro', zero_division=0),
                AUC=roc_auc_score(ytest, prob) if len(np.unique(ytest)) == 2 else np.nan))
    return pd.DataFrame(rows)
