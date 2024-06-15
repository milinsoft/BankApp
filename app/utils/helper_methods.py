from decimal import Decimal
from typing import TypeVar

from app.config import settings

number = TypeVar("number", int, float, Decimal)


# TODO: find a way to remove?
def to_decimal(amount_as_str: number | str, rounding: str = settings.ROUNDING) -> Decimal:
    return Decimal(amount_as_str).quantize(Decimal("0.00"), rounding=rounding)
