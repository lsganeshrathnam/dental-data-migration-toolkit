
import argparse
import sys

from dental_migration.ingestion import DataIngestionError
from dental_migration.migration import run_migration


def main() -> int:
    """Run the dental data migration application."""

    parser = argparse.ArgumentParser(
        description="Dental Data Migration Toolkit"
    )

    parser.add_argument(
        "--input-dir",
        default="data/raw",
        help="Directory containing source CSV files.",
    )

    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory where migration results will be saved.",
    )

    args = parser.parse_args()

    try:
        summary = run_migration(
            raw_data_dir=args.input_dir,
            output_dir=args.output_dir,
        )

    except (FileNotFoundError, DataIngestionError, OSError, ValueError) as exc:
        print(f"\nMigration failed: {exc}", file=sys.stderr)
        return 1

    print("\nDental Data Migration Completed Successfully")
    print("=" * 48)

    print("\nPATIENT SUMMARY")
    print(f"Total patients:        {summary['total_patients']}")
    print(f"Clean patients:        {summary['clean_patients']}")
    print(f"Patients for review:   {summary['patients_for_review']}")

    print("\nAPPOINTMENT SUMMARY")
    print(f"Total appointments:    {summary['total_appointments']}")
    print(f"Clean appointments:    {summary['clean_appointments']}")
    print(f"Appointments for review: {summary['appointments_for_review']}")

    print("\nREPORT")
    print(f"Migration report: {summary['report_path']}")

    print("\nOutput directory: output/")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
