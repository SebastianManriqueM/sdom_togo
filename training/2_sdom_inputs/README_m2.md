![NLR Logo](../../NLR_logo.png)

# 2 — SDOM Inputs and Data Loading

This module explains how SDOM input folders are structured and how to inspect the
Python dictionary produced by `load_data` using the sample scenario.

## Learning objectives

- Identify the core CSV files used by SDOM in `data/sample_data/`.
- Load the input scenario with `sdom.load_data`.
- Explore the resulting dictionary keys, table shapes, and key parameters.
- Verify active formulations before running simulations.

## Prerequisites

- You completed module 1: [training/1_sdom_install/README_m1.md](../1_sdom_install/README_m1.md).
- Your virtual environment is active and SDOM is installed.

## Inputs and scenario used

- Scenario folder: `data/sample_data/`
- Key files used in this module:
  - `formulations.csv`
  - `scalars.csv`
  - `StorageData_2050.csv`
  - `Load_hourly_2050.csv`
  - `CFSolar_2050.csv`, `CFWind_2050.csv`

Reference:
- SDOM input data guide: <https://natlabrockies.github.io/SDOM/user_guide/inputs.html>

## Project/file structure for this module

```text
training/2_sdom_inputs/
├── README_m2.md
└── explore_data.py
```

## Module suffix and script naming

- Module suffix: `m2`
- Script naming note: this data-exploration module keeps `explore_data.py`
   (the `run_mx.py` naming is used in simulation modules).

## Step-by-step walkthrough

1. Activate the environment and run:

   ```powershell
   python training/2_sdom_inputs/explore_data.py
   ```

2. Confirm the script prints:
   - The top-level dictionary keys.
   - Shapes for key data tables.
   - Active formulation selections.
   - Sample values (e.g., `GenMix_Target`).

## Full runnable script

See [training/2_sdom_inputs/explore_data.py](explore_data.py).

## Expected outputs

- A compact inventory of the loaded SDOM data dictionary.
- Printed table shapes for critical input tables.
- A summary of which formulations are active in the sample case.

## How to validate results

- The script should complete without exceptions.
- At least the keys `scalars`, `storage_data`, and `load_data` should appear.
- `GenMix_Target` should be listed from `scalars`.

## Troubleshooting

- `FileNotFoundError`: run the script from repo root, or adjust paths.
- Missing keys in printed output: verify that `data/sample_data/` has all source CSVs.
- Import errors: activate `.venv` before running Python.

## References

- SDOM docs home: <https://natlabrockies.github.io/SDOM/index.html>
- Input data guide: <https://natlabrockies.github.io/SDOM/user_guide/inputs.html>
- API reference (core): <https://natlabrockies.github.io/SDOM/api/core.html>
