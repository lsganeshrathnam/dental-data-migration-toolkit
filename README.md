
# Dental Data Migration Toolkit

A Python-based toolkit for cleaning, validating, and preparing legacy dental practice data for migration into a new practice management system.

The application processes patient and appointment CSV files, standardizes inconsistent values, detects invalid and duplicate records, and generates migration-ready datasets and a data-quality report.

## Features

- **CSV Ingestion:** Loads patient and appointment records and checks required columns.
- **Data Normalization:** Standardizes names, phone numbers, email addresses, appointment statuses, and provider names.
- **Data Validation:** Detects missing fields, invalid dates, malformed email addresses, and invalid phone numbers.
- **Duplicate Detection:** Identifies duplicate patient records and separates conflicting records for manual review.
- **Referential Integrity:** Checks whether appointments reference valid patient records.
- **Migration Exports:** Separates cleaned records from records requiring review.
- **Migration Reporting:** Generates a JSON summary of migration results.
- **Automated Testing:** Includes unit and integration tests using Pytest.

## Technology Stack

- Python 3.11+
- Pandas
- Pytest
- Git and GitHub

## Project Structure

```text
dental-data-migration-toolkit/
│
├── data/
│   └── raw/
│       ├── patients.csv
│       └── appointments.csv
│
├── src/
│   └── dental_migration/
│       ├── __init__.py
│       ├── ingestion.py
│       ├── normalization.py
│       ├── validation.py
│       ├── deduplication.py
│       ├── reporting.py
│       ├── migration.py
│       └── main.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_normalization.py
│   ├── test_validation.py
│   ├── test_deduplication.py
│   └── test_migration.py
│
├── .gitignore
├── pytest.ini
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or later
- pip

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/dental-data-migration-toolkit.git
cd dental-data-migration-toolkit
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -e ".[dev]"
```

### 4. Run the migration

```powershell
python -m dental_migration.main
```

The application uses `data/raw` as its default input directory and `output` as its output directory.

Custom directories can also be specified:

```powershell
python -m dental_migration.main --input-dir data/raw --output-dir output
```

## Input Data

The application expects two CSV files.

### patients.csv

Required columns:

- patient_id
- first_name
- last_name
- phone
- email
- date_of_birth

### appointments.csv

Required columns:

- appointment_id
- patient_id
- appointment_date
- status
- provider

The sample datasets contain intentionally inconsistent records to exercise the cleaning and validation workflows.

## Output Files

After a successful migration, the application generates:

```text
output/
│
├── cleaned/
│   ├── patients_cleaned.csv
│   └── appointments_cleaned.csv
│
├── review/
│   ├── patients_for_review.csv
│   └── appointments_for_review.csv
│
└── reports/
    └── migration_report.json
```

### Cleaned Records

Contains records that passed the implemented validation and duplicate checks.

### Records for Review

Contains records with missing, invalid, or inconsistent information that require manual review.

### Migration Report

The JSON report includes:
- Generation timestamp
- Total patient records
- Clean patient records
- Patient records requiring review
- Total appointment records
- Clean appointment records
- Appointment records requiring review

## Sample Results

Using the included synthetic datasets:

| Metric | Records |
|---|---:|
| Total patients | 6 |
| Clean patients | 2 |
| Patients for review | 4 |
| Total appointments | 5 |
| Clean appointments | 3 |
| Appointments for review | 2 |

These figures represent the included sample data, not a production benchmark.

## Running Tests

Execute the complete test suite:

```powershell
python -m pytest -v
```

The test suite covers:
- CSV ingestion
- Data normalization
- Patient and appointment validation
- Duplicate detection
- End-to-end migration workflow

## Data Privacy

This project uses synthetic sample data only. No real patient information or protected health information (PHI) is included.

The toolkit is a demonstration project and has not been certified for production healthcare or HIPAA-compliant deployments.

## Development

Developed with Python and Pandas, with ChatGPT assistance during implementation and testing.

