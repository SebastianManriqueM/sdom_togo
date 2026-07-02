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

- 2026-07-02: Module 2 README (`training/2_sdom_inputs/README_m2.md`) now documents sample-data file naming conventions, column-ID matching rules, storage-data orientation, and the main purpose of every current input file in `data/sample_data/`.
- 2026-07-02: Training module readmes now use module-suffixed filenames (`README_m1.md` to `README_m5.md`) instead of plain `README.md`.
- 2026-07-02: Training module READMEs (2-5) now include explicit module suffix notes (`m2`-`m5`), and modules 3-5 document that `N_HOURS` is didactic while real studies should use 8760 hours.
- 2026-07-02: Training execution scripts in modules 3–5 now follow `run_mx.py` naming (`run_m3.py`, `run_m4.py`, `run_m5.py`) instead of plain `run.py`.
- 2026-07-02: Cancelling active `ParametricStudy.run()` workers on Windows can surface `concurrent.futures.process.BrokenProcessPool` in remaining cases; this is expected during forced stop, and SDOM may still write `parametric_summary.csv`, partial case outputs, and runtime CSV entries.
- 2026-07-01: Top-level README now serves as workshop-facing documentation, including July 2026 Lome BESS context, module summary for `training/`, and formal acknowledgements.
- 2026-07-01: Training modules should write artifacts to a module-local `sample_output/` folder so outputs are easy to inspect in-place.
- 2026-07-02: Training simulation scripts should use `N_HOURS = 7*24*2` (two weeks) as the didactic time horizon.
- 2026-07-01: Training module README files should include the `NLR_logo.png` image at the top, using a repo-root relative path from each module folder.
- 2026-07-01: Training scripts should include concise explanatory comments and, where relevant, comments linking directly to SDOM documentation pages.
- 2026-07-01: Training content is being organized as a numbered module series under `training/`, and each module should include a structured README with consistent sections plus (for code modules) a runnable companion script.
- _(none yet — populate as you go)_
