# Japan 9-region PyPSA capacity expansion model (FY2040)

**Release candidate for paper reproducibility; NOT yet independently re-solved.**
This package is built from the three files supplied by the authors on 2026-11-03:
`japan9cewg2(2).py`, `input 2.zip`, and `results(1).zip`.

## Contents

- `src/japan9cewg2.py`: exact original model source bytes (no mathematical/code changes).
- `input/`: 9-region time series and WG baseline cost data. Default policy file is neutral (both extra constraints OFF).
- `scenario_data/technology_cost_REI_2040.csv`: REI revised technology costs (REINEW, not REIOLD).
- `cases.json`: deterministic configurations for 6 paper cases.
- `scripts/run_case.py`: prepares per-case inputs without changing tracked data; full optimization is opt-in.
- `scripts/verify_reference.py`: static integrity/consistency checks; requires only pandas.
- `reference_results/`: selected **unaltered** result CSV bytes from original archive plus derived manuscript verification tables.
- `provenance/`: SHA-256 hashes of the original files and discarded alternatives.

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/verify_reference.py
python scripts/run_case.py REI-CO2 --prepare-only
python scripts/run_case.py REI-CO2 --run --overwrite
# Or run all six cases (resource intensive):
python scripts/run_case.py ALL --run --overwrite
# Representative-week sensitivity underlying manuscript Figures 2–3:
python scripts/run_case.py REI-CO2 --time-mode rep4 --run --overwrite
python scripts/run_case.py REI-CO2 --time-mode rep8 --run --overwrite
python scripts/run_case.py REI-CO2 --time-mode rep10 --run --overwrite
# After each fresh run, compare against archived outputs:
python scripts/compare_re_run.py REI-CO2
```

**Use the wrapper** rather than invoking the original script directly. The original Python script defaults to 4 representative weeks and its case label only changes the output folder, not the economic or policy conditions. The wrapper explicitly chooses FY2040 8760-hour mode, cost inputs and active constraints for each case.

**Important**: `--prepare-only` creates `.work/CASE/input/` and writes the case policy and selected cost file, without solving. `--run` executes the original model and logs to `.work/CASE/run.log`. New results are stored under `.work/CASE/results/`. These paths are excluded from Git.

## Six main cases

| Case | Cost source | CO₂ 0.04 t/MWh cap | SEP share limits |
|---|---|---|---|
| WG | WG | OFF | OFF |
| REI | REI revised | OFF | OFF |
| WG-CO2 | WG | ON | OFF |
| REI-CO2 | REI revised | ON | OFF |
| WG-SEP | WG | ON | ON |
| REI-SEP | REI revised | ON | ON |

For all six reference runs, the applied carbon **price** was zero JPY/tCO₂. The CO₂ intensity **constraint** was 0.04 tCO₂/MWh (= 0.04 kgCO₂/kWh) when enabled. Note this distinction. Nuclear 'MID' is reflected in baseline capacity inputs.

## Scope of verification

- Original model Python bytes, unchanged; original input/results ZIP SHA-256 recorded in `provenance/`.
- Reference files retain original raw contents. Only the reference filenames were normalized (original names in `reference_results/source_files.csv`).
- All six result totals round to the paper's 6.8, 6.5, 11.8, 8.3, 12.1 and 10.9 trillion JPY/year respectively.
- CO₂ constraints, annual load and shadow-price values align with the manuscript's text to its stated precision.
- The representative-week 4/8/10-period cost totals also match the paper (10.1 / 9.5 / 9.7 trillion JPY/year).
- The **Figure 4 source TWh table** supplied in the chat is systematically about 25/24 times the raw 8760-hour simulation TWh; this is NOT the correct raw result. See `reference_results/figure4_correction_check.csv` and `reference_results/corrected_generation_TWh.csv`. Generation shares (percent) are essentially unchanged by the common factor. Check whether the draft figure is based on scaled TWh or only percentages.
- The old source ZIP has some mislabeled `SCENARIO_NAME` entries inside original result metadata. Metadata was not edited, since that would destroy source provenance; newly re-run cases will have correct labels through the wrapper.
- With no offshore wind new builds in the REI main cases, output quantities alone cannot distinguish between REIOLD vs REINEW offshore costs. This package explicitly adopts REINEW as the intended analysis source; a full independent re-run is required to prove complete numerical reproducibility.

## Limitations / publication gate

1. **No fresh six-case 8760h optimization rerun was performed here.** PyPSA/HiGHS is required for this, as is sufficient compute time. Reference-number consistency is not a proof of full code reproducibility.
2. `LICENSE_REVIEW_REQUIRED.md` and `docs/DATA_PROVENANCE_REVIEW.md`: Obtain permission for open code licensing and redistribute rights for all source-derived input CSVs before creating a public repository.
3. The current live GitHub branch/commit has NOT been compared or replaced. Back up the existing repository and create a new review branch; avoid force-pushing to the default branch.
4. Some other derived figures in a newer manuscript may have been revised after the available 2026-10-27 draft. Confirm the most recent figures and Tables 7/8 against the corrected CSVs here.
5. Versions `pypsa==1.1.2`, `linopy==0.6.6` reflect the recorded prior environment; record the actually installed `highspy` version during a fresh rerun.

## Suggested safe GitHub replacement workflow

Create a backup tag/branch for the existing repository and clone it locally. Extract this ZIP to a clean working directory and review its contents and licensing. Use `git add -A`, review `git status` and `git diff --stat`, then commit and push a **new review branch**, e.g. `paper-2026-reproducible-release`. Merge only after the static checks, permission review and a fresh six-case computation complete successfully. Do not use `git push --force`.

## Provenance

All original input CSV checksums (plus ignored alternatives) are in `provenance/original_input_manifest.csv`. All embedded reference result CSV checksums and original source locations are in `reference_results/source_files.csv`.

Detailed safe migration instructions for the earlier GitHub repository: `docs/GITHUB_REPLACEMENT_STEPS.md`.
