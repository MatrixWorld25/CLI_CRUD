# Algoryx Task 1 - CLI CRUD Application

## Project Overview

This project is a professional menu-driven command-line CRUD application for managing records with an ID, name, email, phone number, and role. Records are saved in `data/records.json`, so data remains available after the application exits.

## Objectives

- Build a clean interactive CLI.
- Implement create, read, update, delete, and search workflows.
- Persist records safely in JSON.
- Validate user input and handle common errors gracefully.
- Keep the project modular and testable.

## Features

- Create records with duplicate ID protection.
- View all records in readable columns.
- Search by name, email, phone, or role.
- Update records while keeping existing values by pressing Enter.
- Delete records with confirmation.
- Safe JSON file storage.
- Ctrl+C and EOF handling in the CLI.
- Unit tests using temporary storage.

## Technologies

- Python 3
- Standard library only
- `unittest` for tests
- JSON file storage

## Requirements

Python 3.10 or newer is recommended. No third-party package installation is required.

## Project Structure

```text
D:\CLI_CRUD
|-- app
|   |-- __init__.py
|   |-- cli.py
|   |-- config.py
|   |-- models.py
|   |-- repository.py
|   |-- service.py
|   |-- storage.py
|   `-- validators.py
|-- data
|   `-- records.json
|-- tests
|   |-- __init__.py
|   `-- test_service.py
|-- .gitignore
|-- main.py
|-- requirements.txt
|-- README.md
|-- DOCUMENTATION.md
`-- SUBMISSION_GUIDE.md
```

## Installation

```bash
git clone <YOUR_REPOSITORY_URL>
cd CLI_CRUD
```

No dependency install step is needed because the project uses only the Python standard library.

## Running the Application

```bash
python main.py
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## CRUD Explanation

- Create: adds a new validated record.
- Read: lists all records or retrieves a record by ID through the service layer.
- Update: edits an existing record and preserves fields left blank in the CLI.
- Delete: removes an existing record after confirmation.

## JSON Storage Explanation

Records are stored as a JSON list in `data/records.json`. The storage layer reads and writes UTF-8 JSON and uses a temporary file replacement strategy when saving.

## Validation

The application validates positive numeric IDs, required names, valid email format, phone length and characters, and required roles. Duplicate IDs are rejected.

## Exception Handling

The CLI handles validation errors, missing records, storage errors, invalid menu choices, Ctrl+C, and EOF without crashing during normal user mistakes.

## Architecture

The application is split into focused modules:

- `models`: record data structure.
- `validators`: field validation.
- `storage`: JSON persistence.
- `repository`: persistence operations.
- `service`: business rules.
- `cli`: interactive user interface.
- `config`: project paths.

## Example CLI Usage

```text
1. Create record
2. View records
3. Search records
4. Update record
5. Delete record
6. Exit

Select an option: 1
ID: 1
Name: Ayan
Email: ayan@example.com
Phone: +91 9876543210
Role: Developer
```

## GitHub Submission Instructions

Initialize Git, commit the project, push it to a public GitHub repository, create the tag `v1.0.0`, and publish a release. See `SUBMISSION_GUIDE.md` for detailed commands and checklist items.
