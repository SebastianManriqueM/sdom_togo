"""Module 3: single SDOM run with exports and default plots.

Run from repository root:
    python training/3_sdom_single_run/run.py
"""

from __future__ import annotations

from pathlib import Path

from sdom import (
    export_results,
    get_default_solver_config_dict,
    initialize_model,
    load_data,
    run_solver,
)
from sdom.analytic_tools import plot_results

N_HOURS = 1440
CASE_NAME = "training_single_1440"


def assert_optimal(result) -> None:
    """Fail fast if SDOM did not solve optimally."""
    if result.solver_status != "ok" or result.termination_condition != "optimal":
        raise RuntimeError(
            "Solve was not optimal: "
            f"status={result.solver_status}, "
            f"termination={result.termination_condition}"
        )


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    input_dir = repo_root / "data" / "sample_data"
    output_dir = repo_root / "results" / "training" / "3_sdom_single_run"

    # Core SDOM API docs:
    # https://natlabrockies.github.io/SDOM/api/core.html
    data = load_data(input_data_dir=str(input_dir))

    # initialize_model supports partial horizons for faster iteration.
    # https://natlabrockies.github.io/SDOM/user_guide/running_and_outputs.html
    model = initialize_model(data, n_hours=N_HOURS)

    # HiGHS avoids external executable paths in training environments.
    solver_config = get_default_solver_config_dict(solver_name="highs")

    result = run_solver(model, solver_config, case_name=CASE_NAME)
    assert_optimal(result)

    # Export results tables to CSV files.
    # https://natlabrockies.github.io/SDOM/api/io_manager.html
    export_results(result, case=CASE_NAME, output_dir=str(output_dir))

    # Create SDOM default plot pack for this solved case.
    # https://natlabrockies.github.io/SDOM/api/analytic_tools.html
    plot_results(result, output_dir=str(output_dir))

    print("Single run completed successfully.")
    print(f"- solver_status: {result.solver_status}")
    print(f"- termination_condition: {result.termination_condition}")
    print(f"- total_cost: {result.total_cost:,.2f}")

    if hasattr(result, "summary_df") and result.summary_df is not None:
        print("\nSummary table preview:")
        print(result.summary_df.head())


if __name__ == "__main__":
    main()
