# Project Documentation

## Objective

Build a menu-driven Python CLI CRUD application for managing records with persistent JSON storage.

## Requirements

The application supports creating, reading, updating, deleting, and searching records. It validates input, persists data in `data/records.json`, handles common errors, and includes unit tests that do not touch the real data file.

## Architecture

The project uses a layered design:

- CLI handles user interaction.
- Service validates input and applies business rules.
- Repository manages record persistence operations.
- Storage handles JSON file reading and writing.
- Validators contain field-level validation rules.
- Models define the record schema.
- Config defines filesystem paths.

## Folder Structure

```text
app/
data/
tests/
main.py
README.md
DOCUMENTATION.md
SUBMISSION_GUIDE.md
requirements.txt
```

## Module Responsibilities

- `app/models.py`: defines the `Record` dataclass and dictionary conversion.
- `app/config.py`: defines `BASE_DIR`, `DATA_DIR`, and `DATA_FILE`.
- `app/validators.py`: validates ID, name, email, phone, and role.
- `app/storage.py`: implements safe JSON load and save operations.
- `app/repository.py`: provides all, get, create, update, delete, and search persistence methods.
- `app/service.py`: enforces validation and business rules.
- `app/cli.py`: presents the interactive menu and gathers user input.
- `main.py`: builds dependencies and starts the CLI.

## Record Schema

```json
{
  "record_id": 1,
  "name": "Ayan",
  "email": "ayan@example.com",
  "phone": "+91 9876543210",
  "role": "Developer"
}
```

## CRUD Workflow

Create validates all fields and rejects duplicate IDs. Read displays stored records. Update first loads an existing record, then validates any changed fields while preserving blank fields. Delete verifies the target record and requires confirmation in the CLI.

## Search Workflow

Search accepts one query string and checks it case-insensitively against name, email, phone, and role.

## Validation Rules

- ID must be a positive whole number.
- Name is required and must be 100 characters or fewer.
- Email is required and must match a standard email pattern.
- Phone is required, may contain common separators, and must contain 7 to 15 digits.
- Role is required and must be 60 characters or fewer.

## Exception Handling

The application handles invalid input, duplicate IDs, missing records, invalid JSON, file read/write errors, invalid menu options, Ctrl+C, and EOF. Storage errors are reported without exposing a traceback in normal CLI usage.

## Storage Mechanism

`JSONStorage` loads a JSON list from disk. Missing files are initialized as empty lists. Saves are written to a temporary file and then moved into place with `os.replace`.

## Testing

Tests are written with `unittest` in `tests/test_service.py`. They use temporary directories so the real `data/records.json` file is not modified.

Run tests with:

```bash
python -m unittest discover -s tests -v
```

## Manual Verification

Manual smoke testing should cover create, read, search, update, read again, delete, read again, exit, duplicate ID rejection, invalid email, invalid phone, invalid menu option, and deleting a nonexistent record.

## Future Improvements

- Add CSV import/export.
- Add pagination for large record sets.
- Add optional logging.
- Add richer search filters.
