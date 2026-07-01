---
name: sdom-api
description: 'Reference for the SDOM public Python API. Use when writing or reviewing SDOM scripts, choosing between single-run and ParametricStudy, exporting results, or calling analytic_tools plotting functions. Covers load_data, initialize_model, get_default_solver_config_dict, run_solver, export_results, OptimizationResults, ParametricStudy + sweeps, plot_results / plot_parametric_results / zonal plots, and evaluate_resiliency.'
user-invocable: true
---

# SDOM Public API Reference

Authoritative summary of the SDOM public API as installed in this repo's
`.venv`. Always prefer the symbols listed here over any private
(`sdom.models.*`, `_private`) module.

Source of truth: `.venv/Lib/site-packages/sdom/__init__.py` and the official
docs at <https://natlabrockies.github.io/SDOM/>.

## When to use

- Writing any new SDOM script.
- Choosing which API entry point matches a user task.
- Explaining what a specific SDOM function does and how to call it.
- Post-processing an `OptimizationResults` or a list of them.

## Public surface (verified)

### Top-level (`import sdom`)

| Symbol                            | Kind     | Purpose                                          |
| --------------------------------- | -------- | ------------------------------------------------ |
| `configure_logging`               | function | Set logging level / file for SDOM.               |
| `load_data`                       | function | Read all input CSVs of a scenario into a dict.   |
| `initialize_model`                | function | Build a Pyomo model from loaded data.            |
| `get_default_solver_config_dict`  | function | Build the solver-config dict used by `run_solver`. |
| `run_solver`                      | function | Solve the model, return `OptimizationResults`.   |
| `export_results`                  | function | Write CSVs for a solved `OptimizationResults`.   |
| `OptimizationResults`             | class    | Container for all solved-model outputs.          |
| `ParametricStudy`                 | class    | Multi-dimensional sweep runner.                  |
| `evaluate_resiliency`             | function | High-level resiliency-evaluation entry point.    |
| `safe_pyomo_value`                | function | Robustly extract numeric value from a Pyomo var. |

### `sdom.parametric`

| Symbol                | Purpose                                              |
| --------------------- | ---------------------------------------------------- |
| `ParametricStudy`     | Multi-dim study; use `.add_*_sweep()` then `.run()`. |
| `ScalarSweep`         | Sweep a scalar parameter in one data table.          |
| `StorageFactorSweep`  | Multiplicative sweep over a `StorageData` column.    |
| `TsSweep`             | Multiplicative sweep over an hourly time-series.     |

### `sdom.analytic_tools`

| Symbol                          | Purpose                                                    |
| ------------------------------- | ---------------------------------------------------------- |
| `plot_results`                  | Full plot pack for a single `OptimizationResults`.         |
| `plot_parametric_results`       | Grouped/faceted plots across a `ParametricStudy`.          |
| `plot_area_generation_stacks`   | Zonal: stacked hourly generation per area.                 |
| `plot_area_capacity_stacks`     | Zonal: installed-capacity stacks per area (power/energy).  |
| `plot_line_flow_heatmap`        | Zonal: hourly line-flow heatmap.                           |

### `sdom.resiliency`

| Symbol                             | Purpose                                       |
| ---------------------------------- | --------------------------------------------- |
| `evaluate_resiliency`              | End-to-end resiliency evaluation.             |
| `run_resiliency_evaluation`        | Parallel runner (finer control).              |
| `OutageSpec`                       | Declarative outage description.               |
| `MUST_RUN_COMPONENTS`, `VALID_COMPONENTS` | Component-name constants.              |
| `load_cem_data`, `load_designed_system`   | Snapshot loaders.                      |
| `build_baseline_dispatch`, `run_baseline_dispatch` | Baseline dispatch (Problem B). |
| `build_outage_dispatch`            | Outage dispatch (Problem O).                  |
| `add_imports_with_demand_charges`  | Imports formulation with demand charges.      |
| `ResiliencyResults`, `BaselineDispatchResults`, `BaselineState`, `DesignedSystem` | Dataclasses. |
| `plot_metric_distribution`         | Resiliency metric plots.                      |

## Verified signatures

```python
# --- Core ---
sdom.configure_logging(level=20, log_file=None)
sdom.load_data(input_data_dir: str = ".\\Data\\")
sdom.initialize_model(data, n_hours=8760,
                      with_resilience_constraints=False,
                      model_name="SDOM_Model")
sdom.get_default_solver_config_dict(
    solver_name="cbc",
    executable_path=".\\Solver\\bin\\cbc.exe",
    *, mip_gap=0.002, time_limit=None, stream_solver_output=False,
)
sdom.run_solver(model, solver_config_dict: dict,
                case_name: str = "run") -> OptimizationResults
sdom.export_results(results, case: str, output_dir: str = "./results_pyomo/")
sdom.safe_pyomo_value(var)

# --- Parametric ---
sdom.parametric.ParametricStudy(
    base_data: dict, solver_config: dict,
    n_hours: int = 8760,
    output_dir: str | None = None,
    n_cores: int | None = None,
)
ParametricStudy.add_scalar_sweep(data_key: str, param_name: str, values: list)
ParametricStudy.add_storage_factor_sweep(param_name: str, factors: list)
ParametricStudy.add_ts_sweep(ts_key: str, factors: list)
ParametricStudy.run() -> list[OptimizationResults]

# --- Plotting ---
sdom.analytic_tools.plot_results(result, output_dir=None, plots_dir=None)
sdom.analytic_tools.plot_parametric_results(
    study, results, group_by, hue_by=None, facet_by=None,
    output_dir=None, max_cases_per_figure=24, plot_per_case=True,
)
sdom.analytic_tools.plot_area_generation_stacks(results, *, areas=None,
    hours=None, ax=None, save_path=None)
sdom.analytic_tools.plot_area_capacity_stacks(results, *, areas=None,
    mode="power", include_storage=True, orientation="vertical",
    ax=None, save_path=None)
sdom.analytic_tools.plot_line_flow_heatmap(results, *, hours=None,
    normalize_by_capacity=False, ax=None, save_path=None)

# --- Resiliency ---
sdom.evaluate_resiliency(
    snapshot_dir, *, inputs_dir, outage_spec,
    year=2030, scenario_id=1, n_hours=8760, hours=None,
    min_soc_per_tech=None,
    slack_penalty=10_000.0, curtailment_penalty=0.0, soc_slack_penalty=1_000.0,
    formulation_overrides=None, n_workers=None,
    solver="highs", solver_options=None,
    critical_load_MW=None, profile_baseline=False, profile_outages=False,
)
```

## `OptimizationResults` — key attributes

| Attribute                      | Type            | Notes                                          |
| ------------------------------ | --------------- | ---------------------------------------------- |
| `termination_condition`        | `str`           | `"optimal"` on success.                        |
| `solver_status`                | `str`           | `"ok"` on success.                             |
| `total_cost`                   | `float`         | Objective value.                               |
| `gen_mix_target`               | `float`         | Clean-gen target used.                         |
| `generation_df`                | `pd.DataFrame`  | Hourly generation by tech.                     |
| `storage_df`                   | `pd.DataFrame`  | Hourly charge/discharge/SOC.                   |
| `thermal_generation_df`        | `pd.DataFrame`  | Per-thermal-plant hourly generation.           |
| `installed_plants_df`          | `pd.DataFrame`  | Per-plant installed capacity.                  |
| `summary_df`                   | `pd.DataFrame`  | Capacities, costs, totals.                     |
| `problem_info`                 | `dict`          | Solver problem stats.                          |
| `capacity`                     | `dict`          | Capacity by tech.                              |
| `storage_capacity`             | `dict`          | Charge / discharge / energy.                   |
| `generation_totals`            | `dict`          | Total generation by tech.                      |
| `cost_breakdown`               | `dict`          | CAPEX / OPEX / FOM / VOM.                      |
| (zonal) area / line fields     | optional        | Populated only for zonal models.               |

Always check `result.termination_condition == "optimal"` before using
attribute values.

## Canonical single-run recipe

```python
from sdom import (
    load_data, initialize_model,
    get_default_solver_config_dict, run_solver, export_results,
    configure_logging,
)
from sdom.analytic_tools import plot_results

configure_logging()

data   = load_data(input_data_dir="./data/sample_data/")
model  = initialize_model(data, n_hours=8760)
solver = get_default_solver_config_dict(
    solver_name="cbc",
    executable_path="./Solver/bin/cbc.exe",
    mip_gap=0.002,
)

result = run_solver(model, solver, case_name="sample_run")

assert result.termination_condition == "optimal", result.termination_condition
export_results(result, case="sample_run", output_dir="./results/")
plot_results(result, output_dir="./results/sample_run/")
```

## Canonical ParametricStudy recipe

```python
from sdom import load_data, get_default_solver_config_dict
from sdom.parametric import ParametricStudy
from sdom.analytic_tools import plot_parametric_results

data   = load_data(input_data_dir="./data/sample_data/")
solver = get_default_solver_config_dict(solver_name="highs")

study = ParametricStudy(
    base_data=data,
    solver_config=solver,
    n_hours=8760,
    output_dir="./results/param_capex/",
    n_cores=4,
)
study.add_scalar_sweep("scalars", "GenMix_Target", [0.8, 0.9, 1.0])
study.add_storage_factor_sweep("P_Capex", [0.7, 1.0, 1.3])
study.add_ts_sweep("load_data", [0.95, 1.00, 1.05])

results = study.run()  # 3 × 3 × 3 = 27 cases

plot_parametric_results(
    study, results,
    group_by="GenMix_Target",
    hue_by="P_Capex",
    facet_by="load_data_factor",
    output_dir="./results/param_capex/plots/",
)
```

## Do / Don't

- **Do** import from `sdom`, `sdom.parametric`, `sdom.analytic_tools`,
  `sdom.resiliency`.
- **Do** pass explicit `case_name`, `output_dir`, `n_hours`.
- **Do** wrap `study.run()` in a `if __name__ == "__main__":` guard on
  Windows (multiprocessing).
- **Don't** import from `sdom.models.*` or `sdom.optimization_main` directly
  unless you truly need low-level Pyomo access.
- **Don't** silently swallow non-optimal terminations — surface them.

## Related docs

- API index: <https://natlabrockies.github.io/SDOM/api/index.html>
- Core: <https://natlabrockies.github.io/SDOM/api/core.html>
- Results: <https://natlabrockies.github.io/SDOM/api/results.html>
- I/O manager: <https://natlabrockies.github.io/SDOM/api/io_manager.html>
- Parametric: <https://natlabrockies.github.io/SDOM/user_guide/parametric_analysis.html>
- Resiliency: <https://natlabrockies.github.io/SDOM/user_guide/resiliency.html>
- Zonal: <https://natlabrockies.github.io/SDOM/user_guide/zonal_model.html>
- Running & outputs: <https://natlabrockies.github.io/SDOM/user_guide/running_and_outputs.html>
