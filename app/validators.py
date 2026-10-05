"""Validation helpers for record fields."""

from __future__ import annotations

import re

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9\s().-]{6,19}$")


def validate_record_id(value: int | str) -> int:
    """Validate and normalize a record ID."""
    try:
        record_id = int(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError("Record ID must be a whole number.") from exc

    if record_id <= 0:
        raise ValueError("Record ID must be greater than zero.")
    return record_id


def validate_name(value: str) -> str:
    """Validate and normalize a required name."""
    name = value.strip()
    if not name:
        raise ValueError("Name is required.")
    if len(name) > 100:
        raise ValueError("Name must be 100 characters or fewer.")
    return name


def validate_email(value: str) -> str:
    """Validate and normalize an email address."""
    email = value.strip().lower()
    if not email:
        raise ValueError("Email is required.")
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Email must be a valid address, for example name@example.com.")
    return email


def validate_phone(value: str) -> str:
    """Validate and normalize a phone number."""
    phone = " ".join(value.strip().split())
    if not phone:
        raise ValueError("Phone is required.")
    if not PHONE_PATTERN.fullmatch(phone):
        raise ValueError("Phone must be 7 to 20 digits and may include spaces, +, -, parentheses, or dots.")
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 7 or len(digits) > 15:
        raise ValueError("Phone must contain between 7 and 15 digits.")
    return phone


def validate_role(value: str) -> str:
    """Validate and normalize a role."""
    role = value.strip()
    if not role:
        raise ValueError("Role is required.")
    if len(role) > 60:
        raise ValueError("Role must be 60 characters or fewer.")
    return role
