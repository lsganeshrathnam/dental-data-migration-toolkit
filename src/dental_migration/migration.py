
from pathlib import Path

import pandas as pd

from dental_migration.ingestion import load_source_data
from dental_migration.normalization import (
    normalize_patients,
    normalize_appointments,
)
from dental_migration.validation import (
    validate_patients,
    validate_appointments,
)
from dental_migration.deduplication import deduplicate_patients
from dental_migration.reporting import generate_migration_report


def run_migration(
    raw_data_dir: str | Path = "data/raw",
    output_dir: str | Path = "output",
) -> dict:
    """Run the complete dental data migration workflow."""

    # 1. Load source datasets.
    patients, appointments = load_source_data(raw_data_dir)

    # 2. Normalize source records.
    patients = normalize_patients(patients)
    appointments = normalize_appointments(appointments)

    # 3. Validate patient records.
    valid_patients, invalid_patients = validate_patients(patients)

    # 4. Identify duplicate patient records.
    unique_patients, duplicate_patients = deduplicate_patients(
        valid_patients
    )

    # 5. Combine invalid and duplicate patients for review.
    duplicate_patients = duplicate_patients.copy()

    if not duplicate_patients.empty:
        duplicate_patients["review_reason"] = (
            duplicate_patients["duplicate_reason"]
        )
        duplicate_patients = duplicate_patients.drop(
            columns=["duplicate_reason"]
        )
    else:
        duplicate_patients["review_reason"] = pd.Series(dtype="string")

    patient_review = pd.concat(
        [invalid_patients, duplicate_patients],
        ignore_index=True,
    )

    # 6. Validate appointments against unique valid patients.
    valid_patient_ids = set(unique_patients["patient_id"])

    valid_appointments, appointment_review = validate_appointments(
        appointments,
        valid_patient_ids,
    )

    # 7. Create output directories.
    output_dir = Path(output_dir)

    cleaned_dir = output_dir / "cleaned"
    review_dir = output_dir / "review"

    cleaned_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    # 8. Export cleaned records.
    unique_patients.to_csv(
        cleaned_dir / "patients_cleaned.csv",
        index=False,
    )

    valid_appointments.to_csv(
        cleaned_dir / "appointments_cleaned.csv",
        index=False,
    )

    # 9. Export records requiring manual review.
    patient_review.to_csv(
        review_dir / "patients_for_review.csv",
        index=False,
    )

    appointment_review.to_csv(
        review_dir / "appointments_for_review.csv",
        index=False,
    )

    # 10. Create migration summary.
    summary = {
        "total_patients": len(patients),
        "clean_patients": len(unique_patients),
        "patients_for_review": len(patient_review),
        "total_appointments": len(appointments),
        "clean_appointments": len(valid_appointments),
        "appointments_for_review": len(appointment_review),
    }

    # 11. Generate migration report.
    report_path = generate_migration_report(
        summary,
        output_dir / "reports",
    )

    summary["report_path"] = str(report_path)

    return summary
