
import re

import pandas as pd


VALID_APPOINTMENT_STATUSES = {
    "scheduled",
    "completed",
    "cancelled",
}


def _separate_valid_and_review_records(
    data: pd.DataFrame,
    review_reasons: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separate records based on their validation results."""

    result = data.copy()
    result["review_reason"] = review_reasons

    review_mask = result["review_reason"] != ""

    valid_records = (
        result.loc[~review_mask]
        .drop(columns=["review_reason"])
        .copy()
    )

    review_records = result.loc[review_mask].copy()

    return valid_records, review_records


def validate_patients(
    patients: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Validate patient records."""

    review_reasons = []

    for row in patients.to_dict("records"):
        issues = []

        if not row["patient_id"]:
            issues.append("Missing patient ID")

        if not row["first_name"]:
            issues.append("Missing first name")

        if not row["last_name"]:
            issues.append("Missing last name")

        phone = row["phone"]

        if not phone:
            issues.append("Missing phone number")
        elif not re.fullmatch(r"\d{10}", phone):
            issues.append("Invalid phone number")

        email = row["email"]

        if not email:
            issues.append("Missing email address")
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            issues.append("Invalid email address")

        date_of_birth = pd.to_datetime(
            row["date_of_birth"],
            format="%Y-%m-%d",
            errors="coerce",
        )

        if pd.isna(date_of_birth):
            issues.append("Invalid date of birth")

        review_reasons.append("; ".join(issues))

    return _separate_valid_and_review_records(
        patients,
        review_reasons,
    )


def validate_appointments(
    appointments: pd.DataFrame,
    valid_patient_ids: set[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Validate appointments and patient references."""

    review_reasons = []

    valid_patient_ids = {
        str(patient_id).strip()
        for patient_id in valid_patient_ids
    }

    for row in appointments.to_dict("records"):
        issues = []

        if not row["appointment_id"]:
            issues.append("Missing appointment ID")

        patient_id = row["patient_id"]

        if not patient_id:
            issues.append("Missing patient ID")
        elif patient_id not in valid_patient_ids:
            issues.append("Patient ID not found in valid patient records")

        appointment_date = pd.to_datetime(
            row["appointment_date"],
            format="%Y-%m-%d",
            errors="coerce",
        )

        if pd.isna(appointment_date):
            issues.append("Invalid appointment date")

        if row["status"] not in VALID_APPOINTMENT_STATUSES:
            issues.append("Invalid appointment status")

        if not row["provider"]:
            issues.append("Missing provider")

        review_reasons.append("; ".join(issues))

    return _separate_valid_and_review_records(
        appointments,
        review_reasons,
    )
