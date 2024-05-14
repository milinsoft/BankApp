from datetime import date, datetime
from decimal import Decimal
from typing import TypeVar

import settings

number = TypeVar("number", int, float, Decimal)


def date_from_string(date_as_str: str, date_format: str = settings.DATE_FORMAT) -> date:
    try:
        converted_date = datetime.strptime(date_as_str, date_format).date()
    except ValueError:
        raise ValueError(f"Wrong date format! Provided value: {date_as_str} Please use {date_format}")
    if converted_date > date.today():
        raise ValueError("Transaction date is in the future!")
    return converted_date


def to_decimal(amount_as_str: number | str, rounding: str = settings.ROUNDING) -> Decimal:
    return Decimal(amount_as_str).quantize(Decimal("0.00"), rounding=rounding)
