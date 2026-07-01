"""Module 4: simple parametric study with scalar sweep.

Run from repository root:
    python training/4_sdom_parametric_scalar/run.py
"""

from __future__ import annotations

import os
from pathlib import Path

from sdom import get_default_solver_config_dict, load_data
from sdom.analytic_tools import plot_parametric_results
from sdom.parametric import ParametricStudy

N_HOURS = 1440
GENMIX_VALUES = [0.85, 0.95, 1.00]


def safe_n_cores(n_cases: int) -> int:
    """Pick a conservative number of workers for local runs."""
    cpus = os.cpu_count() or 2
    return max(1, min(n_cases, cpus - 1))


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    input_dir = repo_root / "data" / "sample_data"
    output_dir = repo_root / "results" / "training" / "4_sdom_parametric_scalar"

    # Parametric API docs:
    # https://natlabrockies.github.io/SDOM/user_guide/parametric_analysis.html
    data = load_data(input_data_dir=str(input_dir))

    solver_config = get_default_solver_config_dict(solver_name="highs")

    study = ParametricStudy(
        base_data=data,
        solver_config=solver_config,
        n_hours=N_HOURS,
        output_dir=str(output_dir),
        n_cores=safe_n_cores(len(GENMIX_VALUES)),
    )

    # Scalar sweep modifies data["scalars"].loc["GenMix_Target", "Value"].
    # https://natlabrockies.github.io/SDOM/api/core.html
    study.add_scalar_sweep("scalars", "GenMix_Target", GENMIX_VALUES)

    # Note: use __main__ guard on Windows for multiprocessing.
    results = study.run()

    # Plot aggregated trends across sweep values.
    # https://natlabrockies.github.io/SDOM/api/analytic_tools.html
    plot_parametric_results(
        study,
        results,
        group_by="GenMix_Target",
        output_dir=str(output_dir),
    )

    optimal = [r for r in results if r.termination_condition == "optimal"]
    print("Scalar parametric study complete.")
    print(f"- cases_total: {len(results)}")
    print(f"- cases_optimal: {len(optimal)}")
    print(f"- output_dir: {output_dir}")


if __name__ == "__main__":
    main()
