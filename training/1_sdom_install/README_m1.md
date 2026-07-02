![NLR Logo](../../NLR_logo.png)
# 1 — Installing SDOM (Step-by-Step Tutorial)

This tutorial walks you through installing the **Storage Deployment Optimization
Model (SDOM)** on a Windows machine. It is based on the official SDOM
documentation:

- SDOM Documentation home: <https://natlabrockies.github.io/SDOM/index.html>
- Developer / environment setup guide: <https://natlabrockies.github.io/SDOM/sdom_Developers_guide.html>
- SDOM GitHub repository: <https://github.com/NatLabRockies/SDOM>

> SDOM is an open-source, Python/Pyomo-based, high-resolution capacity-expansion
> framework developed by the National Lab of the Rockies (NLR). See the
> [SDOM home page](https://natlabrockies.github.io/SDOM/index.html) for an
> overview.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Install Python](#2-install-python)
3. [Install VS Code and recommended extensions](#3-install-vs-code-and-recommended-extensions)
4. [Install `uv` (Python environment manager)](#4-install-uv-python-environment-manager)
5. [Create a virtual environment](#5-create-a-virtual-environment)
6. [Install SDOM](#6-install-sdom)
    - [Option A — Install from PyPI (end users)](#option-a--install-from-pypi-end-users)
    - [Option B — Install from source (developers)](#option-b--install-from-source-developers)
7. [Install a solver (CBC / HiGHS)](#7-install-a-solver-cbc--highs)
8. [Verify the installation](#8-verify-the-installation)
9. [Quick Start example](#9-quick-start-example)
10. [Troubleshooting](#10-troubleshooting)
11. [References](#11-references)

---

## 1. Prerequisites

Before starting, make sure you have:

- A Windows, macOS or Linux machine with administrator rights.
- An internet connection (to download Python, `uv`, and SDOM).
- ~2 GB of free disk space (Python + virtual env + solver).

Reference: [SDOM Installation — System Setup and Prerequisites](https://natlabrockies.github.io/SDOM/index.html#installation)

---

## 2. Install Python

1. Download Python (3.10 or newer is recommended) from the official site:
   <https://www.python.org/downloads/>
2. Run the installer. **Important**: on the first installer screen, check the
   box **"Add Python to PATH"**.
3. Confirm Python is on your `PATH`. If not, follow this guide to add it:
   <https://realpython.com/add-python-to-path/>
4. Open a new PowerShell window and verify:

    ```powershell
    python --version
    pip --version
    ```

    You should see Python and pip versions printed.

---

## 3. Install VS Code and recommended extensions

SDOM docs recommend [Visual Studio Code](https://code.visualstudio.com/) as the
IDE.

1. Download and install VS Code: <https://code.visualstudio.com/>
2. Install these recommended extensions from the VS Code Marketplace:
    - **Python** (Microsoft)
    - **edit CSV** — to edit SDOM input CSVs directly in VS Code:
      <https://marketplace.visualstudio.com/items?itemName=janisdd.vscode-edit-csv>
    - **vscode-pdf** — to view PDFs inside VS Code:
      <https://marketplace.visualstudio.com/items?itemName=tomoki1207.pdf>

---

## 4. Install `uv` (Python environment manager)

SDOM uses [`uv`](https://pypi.org/project/uv/) to manage virtual environments
and dependencies.

Open PowerShell and run:

```powershell
pip install uv
```

Verify:

```powershell
uv --version
```

Reference: [Install uv](https://natlabrockies.github.io/SDOM/sdom_Developers_guide.html#install-uv)

---

## 5. Create a virtual environment

Choose (or create) a working folder for your SDOM project, `cd` into it, and
create a virtual environment named `.venv`:

```powershell
# Move to your project folder
cd C:\Users\<your-user>\repos\<your-project>

# Create the virtual environment
uv venv .venv

# Activate it (Windows PowerShell)
.venv\Scripts\Activate.ps1
```

For macOS / Linux:

```bash
source .venv/bin/activate
```

When activation succeeds the prompt is prefixed with `(.venv)`.

> If PowerShell blocks script activation, run once (as Administrator):
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

---

## 6. Install SDOM

You have two ways to install SDOM. Pick the one that matches your use case.

With the `.venv` activated:

```powershell
uv pip install sdom
```

---

## 7. Verify the installation

With the virtual environment activated:

```powershell
python -c "import sdom; print(sdom.__version__)"
```

You should see a version number printed (no `ImportError`).

---

## 8. Quick Start example

A minimal SDOM run looks like this (from the [official Quick Start](https://natlabrockies.github.io/SDOM/index.html#installation)):

```python
from sdom import (
    load_data,
    initialize_model,
    run_solver,
    get_default_solver_config_dict,
    export_results,
)

# Load input data
data = load_data("./Data/your_scenario/")

# Initialize model (8760 hours = full year)
model = initialize_model(data, n_hours=8760)

# Configure solver (CBC example)
solver_config = get_default_solver_config_dict(
    solver_name="cbc",
    executable_path="./Solver/bin/cbc.exe",
)

# Solve
results = run_solver(model, solver_config)

if results.is_optimal:
    print(f"Total Cost: ${results.total_cost:,.2f}")
    print(f"Wind Capacity: {results.total_cap_wind:.2f} MW")
    print(f"Solar Capacity: {results.total_cap_pv:.2f} MW")
    export_results(results, case="scenario_1", output_dir="./results/")
```

For details on inputs and outputs, see:

- [SDOM Input Data](https://natlabrockies.github.io/SDOM/user_guide/inputs.html)
- [Running SDOM and Understanding Outputs](https://natlabrockies.github.io/SDOM/user_guide/running_and_outputs.html)

---

## 9a. Inspect SDOM function help from Python

Python's built-in `help()` function prints the docstring and call signature for
any imported SDOM function. This is useful when you want to confirm arguments,
defaults, return values, or expected outputs without leaving the Python session.

From the activated environment, open Python:

```powershell
python
```

Then import the functions used in the quick start and call `help()`:

```python
from sdom import (
  load_data,
  initialize_model,
  get_default_solver_config_dict,
  run_solver,
  export_results,
)

help(load_data)
help(initialize_model)
help(get_default_solver_config_dict)
help(run_solver)
help(export_results)
```

You can also run the same checks without entering the interactive prompt:

```powershell
python -c "from sdom import load_data; help(load_data)"
python -c "from sdom import initialize_model; help(initialize_model)"
python -c "from sdom import get_default_solver_config_dict; help(get_default_solver_config_dict)"
python -c "from sdom import run_solver; help(run_solver)"
python -c "from sdom import export_results; help(export_results)"
```

Expected `help()` output excerpts from this environment:

```text
Help on function load_data in module sdom.io_manager:

load_data(input_data_dir: str = '.\\Data\\')
  Load all required SDOM input datasets from CSV files in the specified directory.

  Reads and validates all input CSV files needed for SDOM optimization including
  VRE data, fixed generation profiles, storage characteristics, thermal units,
  scalars, and formulation specifications. Performs data consistency checks and
  filters datasets based on completeness.
```

```text
Help on function initialize_model in module sdom.optimization_main:

initialize_model(data, n_hours=8760, with_resilience_constraints=False, model_name='SDOM_Model')
  Initialize a Pyomo SDOM optimization model (dispatcher).

  Parameters
  ----------
  data : dict
    Data dictionary as returned by :func:`sdom.io_manager.load_data`.
  n_hours : int, optional
    Number of hours to simulate (default 8760).

  Returns
  -------
  pyomo.environ.ConcreteModel
    A fully initialized Pyomo model ready for optimization, with a
    ``profiler`` attribute attached.
```

```text
Help on function get_default_solver_config_dict in module sdom.optimization_main:

get_default_solver_config_dict(solver_name='cbc', executable_path='.\\Solver\\bin\\cbc.exe', *, mip_gap=0.002, time_limit=None, stream_solver_output=False)
  Generate a default solver configuration dictionary with standard SDOM settings.

  Parameters
  ----------
  solver_name : str, optional
    Solver to use. Supported values: 'cbc', 'highs', and 'xpress'.
  mip_gap : float, optional
    MIP relative optimality gap tolerance. Default is 0.002 (0.2%).
  stream_solver_output : bool, optional
    Whether to stream solver native output live to stdout via ``tee``.
```

```text
Help on function run_solver in module sdom.optimization_main:

run_solver(model, solver_config_dict: dict, case_name: str = 'run') -> sdom.results.OptimizationResults
  Solve the optimization model and return structured results.

  Returns
  -------
  OptimizationResults
    A dataclass containing all optimization results including termination
    condition, total cost, generation dispatch, storage operation, summary
    metrics, capacity, storage capacity, cost breakdown, and problem info.
```

```text
Help on function export_results in module sdom.io_manager:

export_results(results, case: str, output_dir: str = './results_pyomo/')
  Export optimization results to CSV files.

  Output Files
  ------------
  OutputGeneration_{case}.csv
  OutputStorage_{case}.csv
  OutputSummary_{case}.csv
  OutputThermalGeneration_{case}.csv
```

---

## 9. Troubleshooting

- **`uv` is not recognized** — Re-open PowerShell after `pip install uv`, or
  check your `PATH`.
- **Activation script is blocked** — run
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell.
- **`ImportError: sdom`** — make sure the `.venv` is **activated** before
  running Python; the prompt should start with `(.venv)`.
- **Hardlink warning during `uv pip install`** — harmless; you can ignore it
  or set `set UV_LINK_MODE=copy`.
- **Solver not found** — pass an explicit `executable_path` to
  `get_default_solver_config_dict(...)` pointing to your CBC/HiGHS binary.
- See also: [Troubleshooting](https://natlabrockies.github.io/SDOM/user_guide/running_and_outputs.html#troubleshooting).

---

## 11. References

- [SDOM Documentation (home)](https://natlabrockies.github.io/SDOM/index.html)
- [Installation section](https://natlabrockies.github.io/SDOM/index.html#installation)
- [Developer / environment setup guide](https://natlabrockies.github.io/SDOM/sdom_Developers_guide.html)
- [SDOM GitHub repository](https://github.com/NatLabRockies/SDOM)
- [User Guide — Introduction](https://natlabrockies.github.io/SDOM/user_guide/introduction.html)
- [User Guide — Input Data](https://natlabrockies.github.io/SDOM/user_guide/inputs.html)
- [User Guide — Running SDOM and Outputs](https://natlabrockies.github.io/SDOM/user_guide/running_and_outputs.html)
- [API Reference](https://natlabrockies.github.io/SDOM/api/index.html)
- [`uv` on PyPI](https://pypi.org/project/uv/)
- [Python downloads](https://www.python.org/downloads/)
- [VS Code](https://code.visualstudio.com/)
