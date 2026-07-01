---
name: sdom-inputs
description: 'Reference for SDOM input data — folder layout, required CSVs, column conventions, and how formulations.csv toggles which inputs are needed. Use when preparing a new SDOM scenario, validating an existing data folder, adding imports/exports, hydro, nuclear, storage, or switching between copperplate and zonal modes.'
user-invocable: true
---

# SDOM Inputs Reference

Everything an SDOM script needs before `load_data(input_data_dir=...)` will
succeed. Use this skill whenever you touch a folder under `data/`, edit
`formulations.csv`, or scaffold a new scenario.

Authoritative docs:

- Input data structure: <https://natlabrockies.github.io/SDOM/user_guide/inputs.html>
- Zonal inputs: <https://natlabrockies.github.io/SDOM/user_guide/zonal_inputs.html>

## When to use

- Creating a new scenario folder under `data/<scenario>/`.
- Diagnosing a `load_data` / `initialize_model` failure that looks like a
  missing or mis-shaped CSV.
- Deciding whether a scenario needs imports/exports, hydro, nuclear,
  storage, or zonal (multi-area) inputs.
- Reviewing a PR that changes CSVs under `data/`.

## Folder layout

An SDOM scenario is **one folder** of CSVs. Example (from
[`data/sample_data/`](../../../data/sample_data)):

```text
data/<scenario>/
├── formulations.csv          # master switch — which features are active
├── scalars.csv               # global scalar parameters
├── Data_BalancingUnits.csv   # balancing-unit definitions
├── Load_hourly.csv           # 8760-row demand time series
├── CapSolar.csv, CapWind.csv               # VRE resource capacities per site
├── CFSolar.csv,  CFWind.csv                # hourly capacity factors per site
├── StorageData.csv                         # storage tech parameters
├── Nucl_hourly.csv                         # nuclear must-run profile (if used)
├── lahy_hourly.csv, lahy_max_hourly.csv,   # large-hydro profile + bounds
│   lahy_min_hourly.csv
├── otre_hourly.csv                         # other-renewables profile
├── Set_bu(BalancingUnits).txt              # set membership definitions
├── Set_c(Properties).txt
├── Set_k_SolarPV.csv
├── Set_l_Properties.csv
├── Set_w_Wind.csv
└── (zonal) network.csv, area_load.csv, ...  # only when zonal mode is on
```

Optional imports/exports files (from
[`data/sdom_data_request/copperplate/`](../../../data/sdom_data_request/copperplate)):

- `Import_Cap.csv`, `Import_Prices.csv`
- `Export_Cap.csv`, `Export_Prices.csv`
- `Import_time_series.csv` (hourly import limits, if used)

## `formulations.csv` — the master switch

`formulations.csv` enables/disables model features. It is loaded by
`load_data` and consumed by `initialize_model`. Toggling a row **on**
requires the corresponding input CSVs to exist and be well-formed.

Rule of thumb — before enabling a formulation, verify its inputs:

| Formulation family    | Requires (typical)                                                     |
| --------------------- | ---------------------------------------------------------------------- |
| VRE (solar, wind)     | `CapSolar.csv`, `CapWind.csv`, `CFSolar.csv`, `CFWind.csv`, sets       |
| Load                  | `Load_hourly.csv` (8760 rows)                                          |
| Storage               | `StorageData.csv`                                                      |
| Thermal               | thermal capacity/cost columns in `Data_BalancingUnits.csv` / scalars   |
| Hydropower (large)    | `lahy_hourly.csv` + `lahy_min_hourly.csv` + `lahy_max_hourly.csv`      |
| Nuclear (must-run)    | `Nucl_hourly.csv`                                                      |
| Other renewables      | `otre_hourly.csv`                                                      |
| Imports / Exports     | `Import_Cap.csv`, `Import_Prices.csv`, `Export_Cap.csv`, `Export_Prices.csv` |
| Resiliency            | Handled separately by `sdom.evaluate_resiliency`; not a CSV toggle.    |
| Network (zonal)       | Additional per-area CSVs — see zonal inputs docs.                      |

If a formulation row is **off**, do not delete its CSVs — they may still be
consumed by other formulations. Leave them; toggle in `formulations.csv`.

## Hourly time-series conventions

All hourly files use an **8760-row** representation of one year (or a
subset when `n_hours < 8760` is passed to `initialize_model`):

- First column is typically an hour index `1..8760`.
- Subsequent columns are per-site / per-plant / per-tech values.
- No embedded units in headers; units are documented in the
  [inputs docs](https://natlabrockies.github.io/SDOM/user_guide/inputs.html).

## Sets

Set files (`Set_*.txt` / `Set_*.csv`) declare the membership used
throughout the model (balancing units, property lists, solar / wind site
IDs, etc.). Column names and IDs referenced in capacity, cost, or CF files
**must exist** in the corresponding set.

Common breakage: adding a site to `CapSolar.csv` without adding it to
`Set_k_SolarPV.csv` — `initialize_model` will raise a KeyError.

## Zonal vs copperplate

- **Copperplate** (default): single-node system. Uses the file list above.
- **Zonal**: multi-area network. Adds files that describe areas, network
  lines, and per-area load. See
  [Zonal Inputs](https://natlabrockies.github.io/SDOM/user_guide/zonal_inputs.html)
  before scaffolding a zonal case.

## Validation checklist (run mentally before `load_data`)

1. `formulations.csv` present, and every enabled row's CSVs exist.
2. Every hourly file has exactly `n_hours` data rows (or 8760 if using
   defaults).
3. Every ID used in a capacity / cost / CF column also appears in the
   matching `Set_*` file.
4. `scalars.csv` includes `GenMix_Target` (or the scenario's alternative
   target) if the objective depends on it.
5. `StorageData.csv` is present if storage formulation is enabled — even if
   only one technology is defined.
6. Imports/exports files present **iff** the imports/exports formulations
   are on.

## Scaffolding a new scenario

Preferred workflow:

1. Copy an existing well-formed scenario (e.g. `data/sample_data/`) to
   `data/<new_scenario>/`.
2. Edit CSVs in place — never edit `.venv/` or the upstream SDOM repo.
3. Toggle `formulations.csv` **last**, after the CSVs it needs are in
   place.
4. Sanity-run with a small horizon first:

   ```python
   from sdom import load_data, initialize_model
   data  = load_data("./data/<new_scenario>/")
   model = initialize_model(data, n_hours=24)  # 1-day smoke test
   ```

5. Only once that succeeds, run at `n_hours=8760`.

## Related docs

- [Input data structure](https://natlabrockies.github.io/SDOM/user_guide/inputs.html#input-data-structure)
- [Required files](https://natlabrockies.github.io/SDOM/user_guide/inputs.html#required-files)
- [Data validation](https://natlabrockies.github.io/SDOM/user_guide/inputs.html#data-validation)
- [Tips for data preparation](https://natlabrockies.github.io/SDOM/user_guide/inputs.html#tips-for-data-preparation)
- [Zonal conventions](https://natlabrockies.github.io/SDOM/user_guide/zonal_inputs.html#zonal-conventions)
