
from pathlib import Path

import pandas as pd


class DataIngestionError(Exception):
    """Raised when source data cannot be ingested correctly."""


PATIENT_REQUIRED_COLUMNS = {
    "patient_id",
    "first_name",
    "last_name",
    "phone",
    "email",
    "date_of_birth",
}

APPOINTMENT_REQUIRED_COLUMNS = {
    "appointment_id",
    "patient_id",
    "appointment_date",
    "status",
    "provider",
}


def load_csv(
    file_path: str | Path,
    required_columns: set[str],
) -> pd.DataFrame:
    """
    Read a CSV file and verify its required columns.

    All values are initially loaded as strings so that
    identifiers and original values are preserved.
    """
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Source CSV file not found: {file_path}"
        )

    try:
        data = pd.read_csv(
            file_path,
            dtype="string",
            keep_default_na=False,
        )
    except pd.errors.EmptyDataError as exc:
        raise DataIngestionError(
            f"CSV file is empty: {file_path}"
        ) from exc
    except pd.errors.ParserError as exc:
        raise DataIngestionError(
            f"Unable to parse CSV file: {file_path}"
        ) from exc

    # Remove accidental whitespace from column headings.
    data.columns = data.columns.str.strip()

    missing_columns = required_columns.difference(data.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise DataIngestionError(
            f"Missing required columns in {file_path}: {missing}"
        )

    return data


def load_source_data(
    raw_data_dir: str | Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load patient and appointment source datasets."""

    raw_data_dir = Path(raw_data_dir)

    patients = load_csv(
        raw_data_dir / "patients.csv",
        PATIENT_REQUIRED_COLUMNS,
    )

    appointments = load_csv(
        raw_data_dir / "appointments.csv",
        APPOINTMENT_REQUIRED_COLUMNS,
    )

    return patients, appointments