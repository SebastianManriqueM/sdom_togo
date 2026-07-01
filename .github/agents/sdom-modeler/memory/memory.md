# SDOM Modeler — Persistent Memory

Durable, repo-specific notes for the **SDOM Modeler** agent. Read this file at
the start of every task and append to it (with today's date) whenever you learn
something that will help future runs.

## How to use

- Keep entries short: one bullet, one fact.
- Prefer verified facts (things you observed in this repo or in
  `.venv/Lib/site-packages/sdom/**`) over speculation.
- Group by section. Add a new section if none of the existing ones fit.
- When a fact turns out to be wrong, edit or delete the bullet — do not
  leave stale notes.

---

## Repository conventions

- Project root: `sdom_togo/` — SDOM runs for the Togo case study.
- Sample inputs live in [`data/sample_data/`](../../../data/sample_data)
  (copy of the `no_exchange_run_of_river` scenario from the upstream SDOM
  repo).
- Full data request inputs live in
  [`data/sdom_data_request/copperplate/`](../../../data/sdom_data_request/copperplate).
- Results should be written under `results/` (not committed unless
  requested).
- Solver binary is expected at `./Solver/bin/cbc.exe`; if absent, fall back
  to `solver_name="highs"` (installed via `highspy`).

## SDOM version & install

- SDOM package is installed in `.venv` (uv-managed virtual environment).
- Public API is defined in
  `.venv/Lib/site-packages/sdom/__init__.py`; treat that file as the source
  of truth for what is public.

## Public API cheatsheet (verified from `.venv`)

- Top-level: `configure_logging`, `evaluate_resiliency`, `export_results`,
  `get_default_solver_config_dict`, `initialize_model`, `load_data`,
  `OptimizationResults`, `ParametricStudy`, `run_solver`, `safe_pyomo_value`.
- Parametric sweeps: `ScalarSweep`, `StorageFactorSweep`, `TsSweep`.
- Plots: `plot_results`, `plot_parametric_results`,
  `plot_area_generation_stacks`, `plot_area_capacity_stacks`,
  `plot_line_flow_heatmap`, `sdom.resiliency.plot_metric_distribution`.

## Gotchas & lessons learned

<!-- Add dated bullets below. Newest on top. -->

- _(none yet — populate as you go)_
