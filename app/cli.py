"""Interactive command-line interface for the record manager."""

from __future__ import annotations

from collections.abc import Callable

from app.models import Record
from app.service import RecordService
from app.storage import StorageError


class RecordCLI:
    """Menu-driven interface that delegates business logic to RecordService."""

    def __init__(self, service: RecordService) -> None:
        self.service = service
        self.running = True

    def run(self) -> None:
        """Start the interactive menu loop."""
        self._print_header()
        while self.running:
            try:
                self._print_menu()
                choice = input("Select an option: ").strip()
                self._handle_choice(choice)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting safely. Goodbye.")
                self.running = False
            except StorageError as exc:
                print(f"\nStorage error: {exc}")
            except ValueError as exc:
                print(f"\nError: {exc}")

    def _print_header(self) -> None:
        print("=" * 60)
        print("ALGORYX RECORD MANAGER".center(60))
        print("=" * 60)

    def _print_menu(self) -> None:
        print("\n1. Create record")
        print("2. View records")
        print("3. Search records")
        print("4. Update record")
        print("5. Delete record")
        print("6. Exit")

    def _handle_choice(self, choice: str) -> None:
        actions: dict[str, Callable[[], None]] = {
            "1": self._create_record,
            "2": self._view_records,
            "3": self._search_records,
            "4": self._update_record,
            "5": self._delete_record,
            "6": self._exit,
        }

        action = actions.get(choice)
        if action is None:
            print("\nInvalid menu option. Please choose a number from 1 to 6.")
            return
        action()

    def _create_record(self) -> None:
        print("\nCreate Record")
        record = self.service.create_record(
            record_id=self._prompt("ID: "),
            name=self._prompt("Name: "),
            email=self._prompt("Email: "),
            phone=self._prompt("Phone: "),
            role=self._prompt("Role: "),
        )
        print(f"\nRecord {record.record_id} created successfully.")

    def _view_records(self) -> None:
        print("\nView Records")
        print("1. View all records")
        print("2. View record by ID")
        print("Press Enter to return to the main menu.")
        choice = self._prompt("Select an option: ")

        if choice == "1":
            records = self.service.list_records()
            self._display_records(records)
            return
        if choice == "2":
            record_id = self._prompt("ID to view: ")
            record = self.service.get_record(record_id)
            self._display_records([record])
            return
        if choice == "":
            return
        print("\nInvalid read option. Please choose 1, 2, or press Enter.")

    def _search_records(self) -> None:
        print("\nSearch Records")
        query = self._prompt("Search by name, email, phone, or role: ")
        records = self.service.search_records(query)
        self._display_records(records)

    def _update_record(self) -> None:
        print("\nUpdate Record")
        record_id = self._prompt("ID to update: ")
        existing = self.service.get_record(record_id)
        print("Press Enter to keep the current value.")
        updated = self.service.update_record(
            record_id=existing.record_id,
            name=self._optional_prompt(f"Name [{existing.name}]: "),
            email=self._optional_prompt(f"Email [{existing.email}]: "),
            phone=self._optional_prompt(f"Phone [{existing.phone}]: "),
            role=self._optional_prompt(f"Role [{existing.role}]: "),
        )
        print(f"\nRecord {updated.record_id} updated successfully.")

    def _delete_record(self) -> None:
        print("\nDelete Record")
        record_id = self._prompt("ID to delete: ")
        record = self.service.get_record(record_id)
        self._display_records([record])
        confirmation = self._prompt("Delete this record? Type yes to confirm: ").lower()
        if confirmation != "yes":
            print("\nDelete cancelled.")
            return
        self.service.delete_record(record.record_id)
        print(f"\nRecord {record.record_id} deleted successfully.")

    def _exit(self) -> None:
        print("\nGoodbye.")
        self.running = False

    def _prompt(self, message: str) -> str:
        return input(message).strip()

    def _optional_prompt(self, message: str) -> str | None:
        value = input(message).strip()
        return value if value else None

    def _display_records(self, records: list[Record]) -> None:
        if not records:
            print("\nNo records found.")
            return

        print()
        print(f"{'ID':<6} {'Name':<24} {'Email':<30} {'Phone':<18} {'Role':<20}")
        print("-" * 100)
        for record in records:
            print(
                f"{record.record_id:<6} "
                f"{self._clip(record.name, 24):<24} "
                f"{self._clip(record.email, 30):<30} "
                f"{self._clip(record.phone, 18):<18} "
                f"{self._clip(record.role, 20):<20}"
            )

    def _clip(self, value: str, width: int) -> str:
        return value if len(value) <= width else f"{value[: width - 3]}..."
