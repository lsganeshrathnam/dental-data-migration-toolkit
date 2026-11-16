
import pandas as pd


def deduplicate_patients(
    patients: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Identify repeated patient IDs.

    Identical duplicate records: keep the first and send
    subsequent copies for review.

    Conflicting records with the same patient ID: send
    every record in that group for manual review.
    """

    if "patient_id" not in patients.columns:
        raise ValueError("Missing required column: patient_id")

    duplicate_indices = set()
    review_reasons = {}

    duplicate_groups = patients[
        patients.duplicated(subset=["patient_id"], keep=False)
    ]

    for patient_id, group in duplicate_groups.groupby(
        "patient_id",
        sort=False,
    ):
        if len(group.drop_duplicates()) == 1:
            # Records are identical: keep the first copy.
            indices_to_review = group.index[1:]

            for index in indices_to_review:
                duplicate_indices.add(index)
                review_reasons[index] = (
                    "Exact duplicate patient record"
                )

        else:
            # Records share an ID but contain different data.
            # Do not choose a record automatically.
            for index in group.index:
                duplicate_indices.add(index)
                review_reasons[index] = (
                    "Conflicting records share patient ID; "
                    "manual review required"
                )

    unique_records = patients.drop(
        index=list(duplicate_indices)
    ).copy()

    duplicate_records = patients.loc[
        patients.index.isin(duplicate_indices)
    ].copy()

    duplicate_records["duplicate_reason"] = [
        review_reasons[index]
        for index in duplicate_records.index
    ]

    return unique_records, duplicate_records
