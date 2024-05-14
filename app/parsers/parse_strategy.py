from abc import ABC, abstractmethod
from decimal import InvalidOperation
from typing import TYPE_CHECKING

from app.utils.helper_methods import to_decimal

if TYPE_CHECKING:
    from decimal import Decimal

    from app.schemas import STransactionAdd


def parse_trx_amount(amount: str) -> "Decimal":
    try:
        converted_amount = to_decimal(amount)
        if not converted_amount:
            raise ValueError
    except (ValueError, InvalidOperation):
        raise ValueError("Incorrect transaction amount!")
    return converted_amount


def check_description(description: str) -> None:
    if not description:
        raise ValueError("Missing transaction description!")


class AbstractParseStrategy(ABC):
    @classmethod
    @abstractmethod
    def parse_data(cls, file_path: str, account_id: int) -> list["STransactionAdd"]:
        raise NotImplementedError
