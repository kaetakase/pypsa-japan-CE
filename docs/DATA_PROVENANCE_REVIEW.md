# Data provenance and licensing: ACTION REQUIRED

Review each source before making this repository public. The original paper cites REI generation charts,
public electricity and population forecasts, technology cost review sheets and other sources. Some input
files may be derived from sources with redistribution conditions. The provenance text is not a license grant.

Files requiring specific rights confirmation:
- `input/load_2040.csv` (2040 load series and source derivation)
- `input/*_pu_2040.csv` (generation hourly profiles and base-year measurement sources)
- `input/capacity_expansion_2040.csv` (existing capacities and development potentials)
- `input/lines_expansion_2040.csv` (corridor constraints / transmission data)
- `input/technology_cost_2040.csv` and `scenario_data/technology_cost_REI_2040.csv` (technology cost sources)
- `input/emission_factor_2040.csv` and `input/fuel_price_2040.csv`

Do not claim third-party redistributability without author/organization approval.
Input hashes are listed in `provenance/original_input_manifest.csv`.
