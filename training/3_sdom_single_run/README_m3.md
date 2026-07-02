![NLR Logo](../../NLR_logo.png)

# 3 — SDOM Single Run, Outputs, and Default Plots

This module runs SDOM end-to-end on `data/sample_data/`, exports results,
generates default plots, and explores key fields of `OptimizationResults`.

## Learning objectives

- Build and solve an SDOM model using the public API.
- Use `N_HOURS=740` for a practical training horizon in this module.
- Check solve success before post-processing.
- Export CSV outputs and generate default plots.

## Prerequisites

- You completed modules 1 and 2.
- Your environment has `sdom` and a solver (HiGHS recommended for this module).

## Inputs and scenario used

- Scenario folder: `data/sample_data/`
- Time horizon in this training script: 740 time steps
- Solver: HiGHS (`solver_name="highs"`)

Reference:
- Running SDOM and outputs: <https://natlabrockies.github.io/SDOM/user_guide/running_and_outputs.html>

## Project/file structure for this module

```text
training/3_sdom_single_run/
├── README_m3.md
└── run_m3.py
```

## Module suffix and script naming

- Module suffix: `m3`
- Script file: `run_m3.py`

## Computational burden and practical simplifications

One key SDOM advantage is that it can co-optimize both storage power capacity
(MW) and storage duration (energy-to-power relationship). SDOM represents
storage investment with separate power and energy CAPEX terms (`P_Capex` and
`E_Capex`), which improves realism but also increases model complexity.

When many storage technologies are available (with different CAPEX structures
and efficiencies), the optimization can become computationally heavy and harder
to solve.

To reduce computational burden, users can:

- Fix duration for selected technologies by setting
   `Min_Duration = Max_Duration` in `data/sample_data/StorageData_2050.csv`.
- Reduce the number of storage technologies included in
   `data/sample_data/StorageData_2050.csv`.
- Use a combination of both approaches.

## Note on `N_HOURS` in training scripts

`N_HOURS` in the training scripts is a didactic setting to produce lighter
models and faster results. For real planning studies, runs should use a full
year horizon (`8760` hours).

## Step-by-step walkthrough

1. Run the script:

   ```powershell
   python training/3_sdom_single_run/run_m3.py
   ```

2. Inspect terminal output for:
   - Solver status and termination condition.
   - Total cost and selected capacity metrics.

3. Inspect output artifacts under:

   ```text
   results/training/3_sdom_single_run/
   ```

## Full runnable script

See [training/3_sdom_single_run/run_m3.py](run_m3.py).

## Expected outputs

- Exported CSV files for the solved case.
- Default SDOM plots generated via `plot_results`.
- Console summary of key `OptimizationResults` fields.

## How to validate results

- `solver_status == "ok"`
- `termination_condition == "optimal"`
- Output directory contains CSVs and figures.

## Troubleshooting

- Solver error: ensure `highspy` is installed in `.venv`.
- Non-optimal termination: reduce horizon for smoke tests, check data quality.
- Missing output files: confirm script completed after `export_results` and `plot_results`.

## References

- SDOM docs home: <https://natlabrockies.github.io/SDOM/index.html>
- API core: <https://natlabrockies.github.io/SDOM/api/core.html>
- API results: <https://natlabrockies.github.io/SDOM/api/results.html>
- Running and outputs: <https://natlabrockies.github.io/SDOM/user_guide/running_and_outputs.html>
