
import json
from datetime import datetime, timezone
from pathlib import Path


def generate_migration_report(
    summary: dict,
    output_dir: str | Path,
) -> Path:
    """Generate a JSON report for a completed migration."""

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": "Dental Data Migration Toolkit",
        "migration_summary": summary,
    }

    report_path = output_dir / "migration_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return report_path
