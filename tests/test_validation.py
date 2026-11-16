
import pandas as pd

from dental_migration.validation import (
    validate_patients,
    validate_appointments,
)


def test_validate_patients_keeps_valid_records():
    patients = pd.DataFrame([
        {
            "patient_id": "P001",
            "first_name": "John",
            "last_name": "Smith",
            "phone": "4805551234",
            "email": "john@example.com",
            "date_of_birth": "1988-04-12",
        }
    ])

    valid, review = validate_patients(patients)

    assert len(valid) == 1
    assert len(review) == 0


def test_validate_patients_flags_invalid_records():
    patients = pd.DataFrame([
        {
            "patient_id": "P003",
            "first_name": "David",
            "last_name": "Brown",
            "phone": "",
            "email": "bad-email",
            "date_of_birth": "1990-02-30",
        }
    ])

    valid, review = validate_patients(patients)

    assert len(valid) == 0
    assert len(review) == 1

    reason = review.iloc[0]["review_reason"]

    assert "Missing phone number" in reason
    assert "Invalid email address" in reason
    assert "Invalid date of birth" in reason


def test_validate_appointments_keeps_valid_records():
    appointments = pd.DataFrame([
        {
            "appointment_id": "A001",
            "patient_id": "P001",
            "appointment_date": "2026-11-20",
            "status": "scheduled",
            "provider": "Dr. Lee",
        }
    ])

    valid, review = validate_appointments(
        appointments,
        {"P001"},
    )

    assert len(valid) == 1
    assert len(review) == 0


def test_validate_appointments_flags_invalid_records():
    appointments = pd.DataFrame([
        {
            "appointment_id": "A003",
            "patient_id": "P999",
            "appointment_date": "not-a-date",
            "status": "pending",
            "provider": "",
        }
    ])

    valid, review = validate_appointments(
        appointments,
        {"P001"},
    )

    assert len(valid) == 0
    assert len(review) == 1

    reason = review.iloc[0]["review_reason"]

    assert "Patient ID not found" in reason
    assert "Invalid appointment date" in reason
    assert "Invalid appointment status" in reason
    assert "Missing provider" in reason
