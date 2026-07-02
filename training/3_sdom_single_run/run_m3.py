"""Module 3: single SDOM run with exports and default plots.

Run from repository root:
    python training/3_sdom_single_run/run_m3.py
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

from sdom import (
    export_results,
    get_default_solver_config_dict,
    initialize_model,
    load_data,
    run_solver,
)
from sdom.analytic_tools import plot_results

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from training.run_time_report import append_run_timing

N_HOURS = 7*24*2
CASE_NAME = "training_single_740"

logger = logging.getLogger(__name__)


def assert_optimal(result) -> None:
    """Fail fast if SDOM did not solve optimally."""
    if result.solver_status != "ok" or result.termination_condition != "optimal":
        raise RuntimeError(
            "Solve was not optimal: "
            f"status={result.solver_status}, "
            f"termination={result.termination_condition}"
        )


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    repo_root = Path(__file__).resolve().parents[2]
    module_dir = Path(__file__).resolve().parent
    input_dir = repo_root / "data" / "sample_data"
    output_dir = module_dir / "sample_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Core SDOM API docs:
    # https://natlabrockies.github.io/SDOM/api/core.html
    data = load_data(input_data_dir=str(input_dir))

    # initialize_model supports partial horizons for faster iteration.
    # https://natlabrockies.github.io/SDOM/user_guide/running_and_outputs.html
    model = initialize_model(data, n_hours=N_HOURS)

    # HiGHS avoids external executable paths in training environments.
    solver_config = get_default_solver_config_dict(
        solver_name="highs",
        stream_solver_output=True,
    )

    result = run_solver(model, solver_config, case_name=CASE_NAME)
    assert_optimal(result)

    # Export results tables to CSV files.
    # https://natlabrockies.github.io/SDOM/api/io_manager.html
    export_results(result, case=CASE_NAME, output_dir=str(output_dir))

    # Create SDOM default plot pack for this solved case.
    # https://natlabrockies.github.io/SDOM/api/analytic_tools.html
    plot_results(result, output_dir=str(output_dir))

    logger.info("Single run completed successfully.")
    logger.info("solver_status: %s", result.solver_status)
    logger.info("termination_condition: %s", result.termination_condition)
    logger.info("total_cost: %0.2f", result.total_cost)

    if hasattr(result, "summary_df") and result.summary_df is not None:
        logger.info("Summary table preview:\n%s", result.summary_df.head().to_string())


if __name__ == "__main__":
    started_at = datetime.now()
    run_status = "success"
    run_details = ""
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        run_status = "error"
        run_details = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        append_run_timing(
            script_path=Path(__file__).resolve(),
            start_time=started_at,
            end_time=datetime.now(),
            status=run_status,
            details=run_details,
        )
