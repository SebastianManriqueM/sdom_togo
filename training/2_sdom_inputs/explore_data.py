"""Module 2: load and inspect SDOM input data.

Run from repository root:
    python training/2_sdom_inputs/explore_data.py
"""

from __future__ import annotations

from pathlib import Path

from sdom import load_data


def print_table_overview(data: dict, key: str) -> None:
    """Print shape and basic index/column info for one table."""
    if key not in data:
        print(f"- {key}: not present in loaded dictionary")
        return

    table = data[key]
    shape = getattr(table, "shape", None)
    print(f"- {key}: shape={shape}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    input_dir = repo_root / "data" / "sample_data"

    # SDOM input loading docs:
    # https://natlabrockies.github.io/SDOM/user_guide/inputs.html
    data = load_data(input_data_dir=str(input_dir))

    print("Loaded SDOM dictionary keys:")
    for key in sorted(data.keys()):
        print(f"  - {key}")

    print("\nKey table overview:")
    for key in [
        "scalars",
        "formulations",
        "storage_data",
        "load_data",
        "cf_solar",
        "cf_wind",
    ]:
        print_table_overview(data, key)

    print("\nSelected scalar values:")
    scalars = data.get("scalars")
    if scalars is not None and "Value" in scalars.columns:
        for param in ["GenMix_Target", "r", "EUE_max"]:
            if param in scalars.index:
                print(f"- {param}: {scalars.loc[param, 'Value']}")

    print("\nActive formulations:")
    formulations = data.get("formulations")
    if formulations is not None and "Formulation" in formulations.columns:
        # Useful for checking feature toggles before model initialization.
        for component in formulations.index:
            selected = formulations.loc[component, "Formulation"]
            print(f"- {component}: {selected}")


if __name__ == "__main__":
    main()
