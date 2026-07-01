"""Module 2: load and inspect SDOM input data.

Run from repository root:
    python training/2_sdom_inputs/explore_data.py
"""

from __future__ import annotations

import logging
from pathlib import Path

from sdom import load_data


logger = logging.getLogger(__name__)


def print_table_overview(data: dict, key: str) -> None:
    """Print shape and basic index/column info for one table."""
    if key not in data:
        print(f"- {key}: not present in loaded dictionary")
        return

    table = data[key]
    shape = getattr(table, "shape", None)
    print(f"- {key}: shape={shape}")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    repo_root = Path(__file__).resolve().parents[2]
    module_dir = Path(__file__).resolve().parent
    sample_output_dir = module_dir / "sample_output"
    sample_output_dir.mkdir(parents=True, exist_ok=True)
    input_dir = repo_root / "data" / "sample_data"

    # SDOM input loading docs:
    # https://natlabrockies.github.io/SDOM/user_guide/inputs.html
    data = load_data(input_data_dir=str(input_dir))

    lines: list[str] = []

    lines.append("Loaded SDOM dictionary keys:")
    for key in sorted(data.keys()):
        lines.append(f"  - {key}")

    lines.append("\nKey table overview:")
    for key in [
        "scalars",
        "formulations",
        "storage_data",
        "load_data",
        "cf_solar",
        "cf_wind",
    ]:
        if key not in data:
            lines.append(f"- {key}: not present in loaded dictionary")
        else:
            table = data[key]
            shape = getattr(table, "shape", None)
            lines.append(f"- {key}: shape={shape}")

    lines.append("\nSelected scalar values:")
    scalars = data.get("scalars")
    if scalars is not None and "Value" in scalars.columns:
        for param in ["GenMix_Target", "r", "EUE_max"]:
            if param in scalars.index:
                lines.append(f"- {param}: {scalars.loc[param, 'Value']}")

    lines.append("\nActive formulations:")
    formulations = data.get("formulations")
    if formulations is not None and "Formulation" in formulations.columns:
        # Useful for checking feature toggles before model initialization.
        for component in formulations.index:
            selected = formulations.loc[component, "Formulation"]
            lines.append(f"- {component}: {selected}")

    # Persist a text artifact so this module has a visible sample output folder.
    report_path = sample_output_dir / "loaded_data_summary.txt"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for line in lines:
        logger.info(line)
    logger.info("Saved summary to: %s", report_path)


if __name__ == "__main__":
    main()
