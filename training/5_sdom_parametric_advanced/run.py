"""Module 5: advanced parametric study with three sweep dimensions.

Run from repository root:
    python training/5_sdom_parametric_advanced/run.py
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sdom import get_default_solver_config_dict, load_data
from sdom.analytic_tools import plot_parametric_results
from sdom.parametric import ParametricStudy

N_HOURS = 1440
GENMIX_VALUES = [0.85, 0.95, 1.00]
STORAGE_P_CAPEX_FACTORS = [0.8, 1.0, 1.2]
LOAD_SCALE_FACTORS = [0.95, 1.00, 1.05]


def safe_n_cores(n_cases: int) -> int:
    """Pick a conservative number of workers for local runs."""
    cpus = os.cpu_count() or 2
    return max(1, min(n_cases, cpus - 1))


def build_case_summary(study: ParametricStudy, results: list) -> pd.DataFrame:
    """Create a compact per-case table for quick review."""
    rows = []
    metadata = study.case_metadata

    for i, result in enumerate(results):
        meta = metadata[i] if i < len(metadata) else {}
        rows.append(
            {
                "case_name": meta.get("case_name", f"case_{i}"),
                "GenMix_Target": meta.get("GenMix_Target"),
                "P_Capex": meta.get("P_Capex"),
                "load_data": meta.get("load_data"),
                "solver_status": result.solver_status,
                "termination_condition": result.termination_condition,
                "total_cost": getattr(result, "total_cost", None),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    input_dir = repo_root / "data" / "sample_data"
    output_dir = repo_root / "results" / "training" / "5_sdom_parametric_advanced"

    data = load_data(input_data_dir=str(input_dir))
    solver_config = get_default_solver_config_dict(solver_name="highs")

    # SDOM parametric study guide:
    # https://natlabrockies.github.io/SDOM/user_guide/parametric_analysis.html
    n_cases = len(GENMIX_VALUES) * len(STORAGE_P_CAPEX_FACTORS) * len(LOAD_SCALE_FACTORS)
    study = ParametricStudy(
        base_data=data,
        solver_config=solver_config,
        n_hours=N_HOURS,
        output_dir=str(output_dir),
        n_cores=safe_n_cores(n_cases),
    )

    # 1) Sweep clean-generation target.
    study.add_scalar_sweep("scalars", "GenMix_Target", GENMIX_VALUES)

    # 2) Sweep storage power CAPEX row in data["storage_data"].
    study.add_storage_factor_sweep("P_Capex", STORAGE_P_CAPEX_FACTORS)

    # 3) Sweep load time-series scale (ts_key: "load_data").
    # TS key mapping docs are implemented in SDOM parametric mutations.
    study.add_ts_sweep("load_data", LOAD_SCALE_FACTORS)

    # Windows note for multiprocessing:
    # https://docs.python.org/3/library/multiprocessing.html
    results = study.run()

    # Parametric plotting API:
    # https://natlabrockies.github.io/SDOM/api/analytic_tools.html
    plot_parametric_results(
        study,
        results,
        group_by="GenMix_Target",
        hue_by="P_Capex",
        facet_by="load_data",
        output_dir=str(output_dir),
    )

    summary_df = build_case_summary(study, results)
    summary_path = output_dir / "advanced_parametric_case_summary.csv"
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(summary_path, index=False)

    optimal_count = int((summary_df["termination_condition"] == "optimal").sum())
    print("Advanced parametric study complete.")
    print(f"- cases_total: {len(summary_df)}")
    print(f"- expected_cases: {n_cases}")
    print(f"- cases_optimal: {optimal_count}")
    print(f"- summary_csv: {summary_path}")


if __name__ == "__main__":
    main()
