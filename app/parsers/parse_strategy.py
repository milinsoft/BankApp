from abc import ABC, abstractmethod
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import TYPE_CHECKING

import settings

if TYPE_CHECKING:
    from app.domain_classes import TransactionData


def check_description(description: str) -> None:
    if not description:
        raise ValueError("Missing transaction description!")


def convert_str_to_date(date_as_str: str, date_format: str = settings.DATE_FORMAT) -> date:
    try:
        converted_date = datetime.strptime(date_as_str, date_format).date()
    except ValueError:
        raise ValueError(f"Wrong date format! Provided value: {date_as_str} Please use {date_format}")
    if converted_date > date.today():
        raise ValueError("Transaction date is in the future!")
    return converted_date


def convert_str_to_decimal_amount(amount_as_str: str, rounding: str = settings.ROUNDING) -> Decimal:
    try:
        # TODO: refactor duplicate with method defined in tests
        converted_amount = Decimal(amount_as_str).quantize(Decimal("0.00"), rounding=rounding)
        if not converted_amount:
            raise ValueError
    except (ValueError, InvalidOperation):
        raise ValueError("Incorrect transaction amount!")
    return converted_amount


class AbstractParseStrategy(ABC):
    @classmethod
    @abstractmethod
    def parse_data(cls, file_path: str) -> list["TransactionData"]:
        raise NotImplementedError
