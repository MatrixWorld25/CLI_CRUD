"""Application entry point."""

from app.cli import RecordCLI
from app.config import DATA_FILE
from app.repository import RecordRepository
from app.service import RecordService
from app.storage import JSONStorage


def main() -> None:
    """Build application dependencies and start the CLI."""
    storage = JSONStorage(DATA_FILE)
    repository = RecordRepository(storage)
    service = RecordService(repository)
    RecordCLI(service).run()


if __name__ == "__main__":
    main()
