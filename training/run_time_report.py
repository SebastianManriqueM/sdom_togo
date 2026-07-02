"""Utilities to track script runtime metrics for SDOM training modules."""

from __future__ import annotations

import csv
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def append_run_timing(
    *,
    script_path: Path,
    start_time: datetime,
    end_time: datetime,
    status: str,
    details: str = "",
    report_path: Path | None = None,
) -> Path:
    """Append one script execution record to the training runtime CSV report."""
    if report_path is None:
        # script_path points to training/<module>/run.py, so parents[1] is training/
        report_path = script_path.parents[1] / "run_time_report.csv"

    report_path.parent.mkdir(parents=True, exist_ok=True)

    duration_seconds = max(0.0, (end_time - start_time).total_seconds())
    row = {
        "script": script_path.as_posix(),
        "start_time": start_time.isoformat(timespec="seconds"),
        "end_time": end_time.isoformat(timespec="seconds"),
        "duration_seconds": f"{duration_seconds:.2f}",
        "status": status,
        "details": details,
    }

    file_exists = report_path.exists()
    with report_path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "script",
                "start_time",
                "end_time",
                "duration_seconds",
                "status",
                "details",
            ],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    logger.info("Runtime report updated: %s", report_path)
    return report_path
