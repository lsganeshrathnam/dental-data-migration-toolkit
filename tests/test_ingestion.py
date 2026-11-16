
import pytest

from dental_migration.ingestion import (
    DataIngestionError,
    load_csv,
)


def test_load_csv_reads_valid_data(tmp_path):
    """Verify that a valid CSV is loaded correctly."""

    csv_file = tmp_path / "patients.csv"

    csv_file.write_text(
        "patient_id,first_name\n"
        "001,John\n",
        encoding="utf-8",
    )

    data = load_csv(
        csv_file,
        {"patient_id", "first_name"},
    )

    assert len(data) == 1
    assert data.loc[0, "patient_id"] == "001"
    assert data.loc[0, "first_name"] == "John"


def test_load_csv_rejects_missing_columns(tmp_path):
    """Verify that missing required columns are detected."""

    csv_file = tmp_path / "patients.csv"

    csv_file.write_text(
        "patient_id,first_name\n"
        "P001,John\n",
        encoding="utf-8",
    )

    with pytest.raises(DataIngestionError):
        load_csv(
            csv_file,
            {"patient_id", "first_name", "email"},
        )


def test_load_csv_rejects_missing_file(tmp_path):
    """Verify that a missing source file raises an error."""

    csv_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_csv(csv_file, {"patient_id"})


def test_load_csv_rejects_empty_file(tmp_path):
    """Verify that an empty CSV raises a clear error."""

    csv_file = tmp_path / "empty.csv"

    csv_file.write_text("", encoding="utf-8")

    with pytest.raises(DataIngestionError):
        load_csv(csv_file, {"patient_id"})