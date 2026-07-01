![NLR Logo](../../NLR_logo.png)

# 5 — Advanced Parametric Study (Scalar + Storage + Time Series)

This module builds an advanced multi-dimensional parametric study with three
sweep types: scalar target, storage cost factor, and load time-series scaling.

## Learning objectives

- Combine multiple sweep dimensions in one `ParametricStudy`.
- Understand Cartesian case expansion and runtime implications.
- Use 1440 time steps for practical training run time.
- Generate comparative plots and a compact case summary table.

## Prerequisites

- You completed modules 1–4.
- You can run SDOM studies with multiprocessing on your platform.

## Inputs and scenario used

- Scenario folder: `data/sample_data/`
- Scalar sweep: `GenMix_Target`
- Storage factor sweep: `P_Capex` row in storage data
- Time-series sweep: `load_data` (`Load` column)
- Time horizon: 1440 time steps

Reference:
- Parametric analysis user guide: <https://natlabrockies.github.io/SDOM/user_guide/parametric_analysis.html>

## Project/file structure for this module

```text
training/5_sdom_parametric_advanced/
├── README.md
└── run.py
```

## Step-by-step walkthrough

1. Run:

   ```powershell
   python training/5_sdom_parametric_advanced/run.py
   ```

2. Confirm total cases equals the product of sweep lengths.
3. Inspect generated outputs under:

   ```text
   results/training/5_sdom_parametric_advanced/
   ```

4. Review the summary CSV with case-level metrics.

## Full runnable script

See [training/5_sdom_parametric_advanced/run.py](run.py).

## Expected outputs

- Multi-case study outputs for all sweep combinations.
- Parametric plots grouped by `GenMix_Target` and hue by `P_Capex` factor.
- A compact case summary CSV.

## How to validate results

- `cases_total = len(genmix) * len(storage_factors) * len(load_factors)`
- Summary CSV exists and has one row per case.
- At least one case solves optimally.

## Troubleshooting

- Slow runtime: reduce sweep dimensions for smoke tests.
- Worker failures: inspect case logs in output folder.
- Plot issues: confirm there are successful cases in the result list.

## References

- SDOM docs home: <https://natlabrockies.github.io/SDOM/index.html>
- Parametric user guide: <https://natlabrockies.github.io/SDOM/user_guide/parametric_analysis.html>
- API core: <https://natlabrockies.github.io/SDOM/api/core.html>
- Running and outputs: <https://natlabrockies.github.io/SDOM/user_guide/running_and_outputs.html>
