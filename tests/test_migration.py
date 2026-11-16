
import json

import pandas as pd

from dental_migration.migration import run_migration


def test_complete_migration_workflow(tmp_path):
    # Create temporary input and output directories.
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "output"

    raw_dir.mkdir()

    # Create sample patient records.
    patients_csv = """patient_id,first_name,last_name,phone,email,date_of_birth
P001,John,Smith,4805551234,john@example.com,1988-04-12
P002,Sarah,Jones,4805552222,sarah@example.com,1992-09-03
P002,SARAH,Jones,(480) 555-2222,sarah@example.com,1992-09-03
P003,David,Brown,,david@example.com,1975-12-21
"""

    # Create sample appointment records.
    appointments_csv = """appointment_id,patient_id,appointment_date,status,provider
A001,P001,2026-11-20,scheduled,Dr. Lee
A002,P003,2026-11-21,scheduled,Dr. Kim
A003,P999,not-a-date,scheduled,Dr. Lee
"""

    (raw_dir / "patients.csv").write_text(
        patients_csv,
        encoding="utf-8",
    )

    (raw_dir / "appointments.csv").write_text(
        appointments_csv,
        encoding="utf-8",
    )

    # Run the complete migration.
    summary = run_migration(
        raw_data_dir=raw_dir,
        output_dir=output_dir,
    )

    # Verify migration counts.
    assert summary["total_patients"] == 4
    assert summary["clean_patients"] == 2
    assert summary["patients_for_review"] == 2

    assert summary["total_appointments"] == 3
    assert summary["clean_appointments"] == 1
    assert summary["appointments_for_review"] == 2

    # Verify all output files were generated.
    expected_files = [
        output_dir / "cleaned" / "patients_cleaned.csv",
        output_dir / "cleaned" / "appointments_cleaned.csv",
        output_dir / "review" / "patients_for_review.csv",
        output_dir / "review" / "appointments_for_review.csv",
        output_dir / "reports" / "migration_report.json",
    ]

    for file_path in expected_files:
        assert file_path.is_file()

    # Verify the cleaned datasets.
    clean_patients = pd.read_csv(
        output_dir / "cleaned" / "patients_cleaned.csv"
    )

    clean_appointments = pd.read_csv(
        output_dir / "cleaned" / "appointments_cleaned.csv"
    )

    assert len(clean_patients) == 2
    assert len(clean_appointments) == 1

    # Verify the generated JSON report.
    report_path = output_dir / "reports" / "migration_report.json"

    report = json.loads(
        report_path.read_text(encoding="utf-8")
    )

    assert report["project"] == "Dental Data Migration Toolkit"
    assert report["migration_summary"]["total_patients"] == 4
    assert report["migration_summary"]["clean_patients"] == 2
