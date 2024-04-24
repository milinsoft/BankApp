from collections.abc import Sequence
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import TYPE_CHECKING

import settings

if TYPE_CHECKING:
    from app.models import TransactionData


class ParseStrategy:
    @classmethod
    def parse_data(cls, file_path) -> Sequence["TransactionData"]:
        raise NotImplementedError

    @classmethod
    def _convert_date(cls, trx_date: str) -> date:
        try:
            converted_date = datetime.strptime(trx_date, settings.DATE_FORMAT).date()
        except ValueError:
            raise ValueError(f"wrong date format! Please use {settings.DATE_FORMAT}")
        if converted_date > date.today():
            raise ValueError("Transaction date is in the future!")
        return converted_date

    @classmethod
    def _convert_amount(cls, trx_amount: str) -> Decimal:
        try:
            converted_amount = Decimal(trx_amount).quantize(Decimal("0.00"), rounding=settings.ROUNDING)
            if not converted_amount:
                raise ValueError
        except (ValueError, InvalidOperation):
            raise ValueError("Incorrect transaction amount!")
        return converted_amount

    @classmethod
    def _check_description(cls, description: str) -> None:
        if not description:
            raise ValueError("Missing transaction description!")
