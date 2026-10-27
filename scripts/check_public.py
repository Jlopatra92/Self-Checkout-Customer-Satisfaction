"""Reject saved outputs and unexpected private assets before staging or packaging."""
from pathlib import Path
import ast
import nbformat
import subprocess
import shutil

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'README.md','requirements.txt','requirements-lock.txt','.gitignore',
           'src/__init__.py','src/analysis.py','scripts/build_notebook.py',
           'scripts/run_notebook.py','scripts/check_public.py',
           'notebooks/01_self_checkout_customer_satisfaction.ipynb',
           'docs/DATA_PROVENANCE.md','docs/GITHUB_GUIDE.md',
           'docs/RESULTS.md','docs/NARRATIVE_REVIEW.md',
           'docs/VALIDATION.md','docs/WORKING_NOTEBOOK_REVIEW.md','data/raw/.gitkeep','outputs/.gitkeep'}

def check():
    for rel in ALLOWED:
        assert (ROOT / rel).is_file(), f'Missing public file: {rel}'
    nb = nbformat.read(ROOT / 'notebooks/01_self_checkout_customer_satisfaction.ipynb',as_version=4)
    nbformat.validate(nb)
    for cell in nb.cells:
        if cell.cell_type == 'code':
            assert not cell.outputs and cell.execution_count is None, 'Saved outputs in public notebook'
            ast.parse(cell.source)
    for path in ROOT.rglob('*.py'):
        if not any(p in path.parts for p in ['.venv','__pycache__']): ast.parse(path.read_text())
    git = shutil.which('git')
    if git:
        repo = subprocess.run([git, '-C', str(ROOT), 'rev-parse', '--show-toplevel'],
                              capture_output=True, text=True)
        if repo.returncode == 0 and Path(repo.stdout.strip()).resolve() == ROOT:
            tracked = subprocess.check_output([git, '-C', str(ROOT), 'ls-files', '-z']).decode().split('\0')
            unexpected = set(filter(None, tracked)) - ALLOWED
            assert not unexpected, f'Non-allowlisted staged/tracked files: {sorted(unexpected)}'
    print('Public notebook schema and syntax valid; no saved outputs. Packaging allowlist:',len(ALLOWED),'files.')
    return sorted(ALLOWED)

if __name__ == '__main__': check()
