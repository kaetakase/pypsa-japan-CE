# Paper alignment audit (as of 2026-11-03)

Baseline: October 27 draft of the manuscript and the author's latest Figure 4 TWh source screenshot (2026-11-03 chat).

## Verified
- Cost totals of all six main cases (rounding to 0.1 trillion JPY/year).
- CO2 intensity in WG and REI unconstrained cases and binding 0.04 intensity in four constrained cases.
- CO2 shadow prices (3.6, 2.5, 4.0, 3.5 x 10,000 JPY/tCO2).
- SEP shadow-price table: WG-SEP wind and geothermal, REI-SEP solar, wind and geothermal. Corrected results in reference_results/table7_shadow_prices.csv.
- REI-CO2 capacity-upper-bound shadow prices (Table 8) in reference_results/table8_capacity_shadow.csv.

## Must correct / check
- Figure 4 TWh table supplied by the author was inflated approximately 25/24 relative to original model generation_summary. The raw result TWh is documented in reference_results/corrected_generation_TWh.csv. An Excel report includes full cell-by-cell differences.
- Older manuscript Figure 4 currently groups onshore/offshore wind, whereas the newer chart splits the three types. Use the new labels and recalculated values.
- Reference result metadata has incorrect internal scenario labels in some cases; original data is preserved with warning.
- The manuscript appears to describe 1100 TWh for ten Japanese regions; computed *nine-region* annual load is 1090.416652 TWh. This is consistent in scale but should be described precisely as model-area coverage.
- Confirm the latest manuscript document (not only the October 27 draft), especially whether its new Table 8 and Figure 4 are now updated.

## Verification limitation
The script source and inputs were statically checked against archived outputs; they were NOT reoptimized on a fresh solver.
