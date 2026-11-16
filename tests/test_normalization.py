
import pandas as pd

from dental_migration.normalization import (
    normalize_patients,
    normalize_appointments,
)


def test_normalize_patients():
    patients = pd.DataFrame({
        "patient_id": [" P001 "],
        "first_name": [" JOHN "],
        "last_name": ["SMITH "],
        "phone": ["(480) 555-2222"],
        "email": ["JOHN.SMITH@EXAMPLE.COM"],
        "date_of_birth": ["1988-04-12"],
    })

    normalized = normalize_patients(patients)

    assert normalized.loc[0, "patient_id"] == "P001"
    assert normalized.loc[0, "first_name"] == "John"
    assert normalized.loc[0, "last_name"] == "Smith"
    assert normalized.loc[0, "phone"] == "4805552222"
    assert normalized.loc[0, "email"] == "john.smith@example.com"

    # Verify that the original DataFrame remains unchanged.
    assert patients.loc[0, "first_name"] == " JOHN "


def test_normalize_appointments():
    appointments = pd.DataFrame({
        "appointment_id": [" A001 "],
        "patient_id": [" P001 "],
        "appointment_date": ["2026-11-20"],
        "status": [" SCHEDULED "],
        "provider": ["  Dr.   Lee  "],
    })

    normalized = normalize_appointments(appointments)

    assert normalized.loc[0, "appointment_id"] == "A001"
    assert normalized.loc[0, "patient_id"] == "P001"
    assert normalized.loc[0, "status"] == "scheduled"
    assert normalized.loc[0, "provider"] == "Dr. Lee"

    # Verify that the original DataFrame remains unchanged.
    assert appointments.loc[0, "provider"] == "  Dr.   Lee  "
