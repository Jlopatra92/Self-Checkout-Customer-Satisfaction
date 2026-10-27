# Step-by-step GitHub publication guide

**Current status:** the author approved creation of the private repository `Jlopatra92/self-checkout-customer-satisfaction`, and it has been created. The steps below remain a guide for uploading and future copies; another repository should not be created for this project. Respondent-level data publication requires separate explicit permission and a privacy/consent review; choosing a private repository does not itself authorize uploading data.

## 1. Review the finished local project

Open the clean notebook and `docs/RESULTS.md`. Use the private executed notebook in `outputs/` for detailed review. Resolve or accept the documented provenance limits, select your narrative, and confirm which aggregate findings may be publicly shared. Keep your original working notebook separately.

The public ZIP contains only allowlisted code, the clean notebook, and documentation. It contains no input workbook or executed outputs. Do not use a full-folder ZIP of the private workspace for upload.

## 2. Choose a repository and authenticate

Suggested repository name: `self-checkout-customer-satisfaction`. Choose **Private** for initial review if you prefer. The GitHub website requires signing in. GitHub Desktop requires its browser sign-in flow. GitHub CLI requires an authenticated account with permission to create repositories; run `gh auth login` locally and complete the browser flow. Do not paste passwords or access tokens into this chat. A connector sign-in does not necessarily authenticate your local terminal.

## 3. Preferred point-and-click option

1. Extract the public ZIP into a new folder, separate from the private analysis folder.
2. Sign in to GitHub → **+** → **New repository**.
3. Enter the agreed name, description, and visibility. Create the empty repository.
4. Choose **uploading an existing file** (or **Add file → Upload files**). Drag the extracted folder contents, preserving `src`, `docs`, `scripts`, `notebooks`, `data/raw`, and `outputs` subfolders.
5. Hidden files such as `.gitignore` can be omitted by a browser drag operation. Verify `.gitignore` is present; add it manually through **Add file → Create new file** if necessary, copying the supplied content. GitHub Desktop is easier for preserving hidden files.
6. Review the file list: no Excel/CSV data, executed notebook, private outputs, source thesis, or credentials. Commit the reviewed files.
7. Open the notebook on GitHub and confirm the source renders and the relative README links work. Its empty outputs are intentional; aggregate results are in the documentation.

## 4. Terminal alternative, after approval

Run these in the extracted public package, not in an unrelated portfolio repository:

```bash
git init -b main
python scripts/check_public.py
git add README.md requirements.txt requirements-lock.txt .gitignore src scripts docs notebooks data/raw/.gitkeep outputs/.gitkeep
git diff --cached --stat
git diff --cached --name-only
git commit -m "Add reproducible self-checkout thesis reanalysis"
```

If Git asks for your author name/email, configure your chosen identity locally; use your GitHub no-reply address if desired. Do not invent an email.

Then, only when the repository name and visibility are approved:

```bash
gh auth login
gh repo create self-checkout-customer-satisfaction --private --source=. --remote=origin --push
```

Change `--private` to `--public` only after choosing public visibility. If creating via the website instead, copy its actual remote URL and use the commands it supplies; replace example placeholders before execution. Never add data with `git add -f`.

## 5. Future updates

Run analyses privately, keep outputs under ignored `outputs/`, and stage only the clean source notebook. If you run and save the public notebook interactively, regenerate it with `python scripts/build_notebook.py`, then run `python scripts/check_public.py`. Review diffs before pushing. Do not add a data license or release source documents until ownership and permissions are confirmed.

Reference: [GitHub's official guide to adding locally hosted code](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github).
