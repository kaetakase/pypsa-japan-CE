# Safe replacement of existing GitHub repository

Repository discussed previously: `kaetakase/pypsa-japan-capacity-expansion` (historically private and using `main`).
The remote contents have **not** been downloaded or compared in this audit. Do not assume that main still contains the same files.

## Recommended workflow

1. Save the current HEAD SHA, back up existing main and record the old structure. Work in a fresh local clone.

```bash
git clone git@github.com:kaetakase/pypsa-japan-capacity-expansion.git
cd pypsa-japan-capacity-expansion
git status --short
git switch main
git pull --ff-only
git branch backup-before-paper-release
git switch -c paper-2026-reproducible-release
```

2. Extract the release ZIP **outside** the clone. Review its `README_ja.md`, `LICENSE_REVIEW_REQUIRED.md` and `docs/DATA_PROVENANCE_REVIEW.md`. Do not blindly overwrite `.git` or `LICENSE`.
3. Compare the release root against the existing working tree (`diff -qr RELEASE_DIR .` or your diff tool). The old repository may contain `scenarios/scenario_matrix.csv` and `scripts/run_scenarios.py`; these are superseded by this package's `cases.json` and `scripts/run_case.py`. Remove them only after identifying other references.
4. To completely replace tracked sources on the **new branch**, remove the previous tracked files from the working tree (preserving the `.git` directory), copy the reviewed new release contents into the repository root, and run:

```bash
python scripts/verify_reference.py
git status --short
git diff --stat
git diff --check
git add -A
git diff --cached --stat
git commit -m "Prepare verified 2040 nine-region PyPSA model and paper references"
git push -u origin paper-2026-reproducible-release
```

5. Open a pull request into `main`. Compare the changed-file list, confirm licensing/provenance, and independently rerun all six 8760h cases and the 4/8/10 representative-week analyses before merging.
6. For archival completeness, attach the original `results(1).zip` (64 MB) to a GitHub Release rather than storing a duplicated 64 MB binary inside normal Git history. This release ZIP already contains the main publication tables and selected raw result CSVs.

Do **not** use `git push --force`, and do not delete the old remote repository. Keep the backup branch and tag an immutable paper release only after verification.
