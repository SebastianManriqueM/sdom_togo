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
