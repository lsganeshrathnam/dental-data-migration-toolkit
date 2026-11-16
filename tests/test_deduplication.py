
import pandas as pd
import pytest

from dental_migration.deduplication import deduplicate_patients


def test_identical_duplicates_keep_one_record():
    patients = pd.DataFrame([
        {
            "patient_id": "P002",
            "first_name": "Sarah",
            "last_name": "Jones",
            "email": "sarah@example.com",
        },
        {
            "patient_id": "P002",
            "first_name": "Sarah",
            "last_name": "Jones",
            "email": "sarah@example.com",
        },
    ])

    unique, duplicates = deduplicate_patients(patients)

    assert len(unique) == 1
    assert len(duplicates) == 1
    assert duplicates.iloc[0]["duplicate_reason"] == (
        "Exact duplicate patient record"
    )


def test_conflicting_duplicates_go_to_review():
    patients = pd.DataFrame([
        {
            "patient_id": "P002",
            "first_name": "Sarah",
            "last_name": "Jones",
            "email": "sarah@example.com",
        },
        {
            "patient_id": "P002",
            "first_name": "Sarah",
            "last_name": "Jones",
            "email": "different@example.com",
        },
    ])

    unique, duplicates = deduplicate_patients(patients)

    assert len(unique) == 0
    assert len(duplicates) == 2
    assert all(
        "Conflicting records" in reason
        for reason in duplicates["duplicate_reason"]
    )


def test_unique_patients_remain_unchanged():
    patients = pd.DataFrame([
        {
            "patient_id": "P001",
            "first_name": "John",
        },
        {
            "patient_id": "P002",
            "first_name": "Sarah",
        },
    ])

    unique, duplicates = deduplicate_patients(patients)

    assert len(unique) == 2
    assert len(duplicates) == 0


def test_missing_patient_id_column_is_rejected():
    patients = pd.DataFrame({
        "first_name": ["John"],
        "last_name": ["Smith"],
    })

    with pytest.raises(ValueError):
        deduplicate_patients(patients)
