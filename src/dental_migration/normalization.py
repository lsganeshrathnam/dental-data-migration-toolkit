
import pandas as pd


def normalize_patients(patients: pd.DataFrame) -> pd.DataFrame:
    """Standardize patient records without modifying the original data."""

    normalized = patients.copy()

    # Remove leading and trailing whitespace.
    text_columns = [
        "patient_id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "date_of_birth",
    ]

    for column in text_columns:
        normalized[column] = normalized[column].str.strip()

    # Standardize names.
    normalized["first_name"] = normalized["first_name"].str.title()
    normalized["last_name"] = normalized["last_name"].str.title()

    # Standardize email addresses.
    normalized["email"] = normalized["email"].str.lower()

    # Keep only digits in phone numbers.
    normalized["phone"] = normalized["phone"].str.replace(
        r"\D", "", regex=True
    )

    return normalized


def normalize_appointments(
    appointments: pd.DataFrame,
) -> pd.DataFrame:
    """Standardize appointment records."""

    normalized = appointments.copy()

    text_columns = [
        "appointment_id",
        "patient_id",
        "appointment_date",
        "status",
        "provider",
    ]

    for column in text_columns:
        normalized[column] = normalized[column].str.strip()

    # Standardize appointment status.
    normalized["status"] = normalized["status"].str.lower()

    # Remove extra spaces within provider names.
    normalized["provider"] = normalized["provider"].str.replace(
        r"\s+", " ", regex=True
    )

    return normalized