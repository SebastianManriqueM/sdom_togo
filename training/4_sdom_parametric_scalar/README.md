![NLR Logo](../../NLR_logo.png)

# 4 — Simple Parametric Study (Scalar Sweep)

This module performs a simple parametric study by sweeping the scalar
`GenMix_Target` and plotting the resulting trends.

## Learning objectives

- Set up a `ParametricStudy` from baseline SDOM inputs.
- Sweep a scalar parameter with `add_scalar_sweep`.
- Run a multi-case study with explicit output paths.
- Plot and inspect parametric results.

## Prerequisites

- You completed modules 1–3.
- You can run SDOM with HiGHS in your environment.

## Inputs and scenario used

- Scenario folder: `data/sample_data/`
- Swept scalar: `scalars -> GenMix_Target`
- Time horizon: 1440 time steps

Reference:
- Parametric analysis: <https://natlabrockies.github.io/SDOM/user_guide/parametric_analysis.html>

## Project/file structure for this module

```text
training/4_sdom_parametric_scalar/
├── README.md
└── run.py
```

## Step-by-step walkthrough

1. Run:

   ```powershell
   python training/4_sdom_parametric_scalar/run.py
   ```

2. Review case-level completion messages and final summary.
3. Inspect outputs in:

   ```text
   results/training/4_sdom_parametric_scalar/
   ```

## Full runnable script

See [training/4_sdom_parametric_scalar/run.py](run.py).

## Expected outputs

- One SDOM result per scalar value.
- Exported per-case CSVs and a study summary.
- Parametric plots grouped by `GenMix_Target`.

## How to validate results

- Number of returned results equals number of scalar values.
- At least one case is optimal (`termination_condition == "optimal"`).
- Plot files are created in the module output directory.

## Troubleshooting

- Multiprocessing issue on Windows: keep the `if __name__ == "__main__":` guard.
- Empty plots: verify at least one successful case.
- Slow runs: reduce number of sweep values for quick tests.

## References

- SDOM docs home: <https://natlabrockies.github.io/SDOM/index.html>
- Parametric user guide: <https://natlabrockies.github.io/SDOM/user_guide/parametric_analysis.html>
- API core: <https://natlabrockies.github.io/SDOM/api/core.html>
