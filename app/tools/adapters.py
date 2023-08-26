from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Tuple

from app.models import Transaction
from settings import DATE_FORMAT


class TransactionsAdapter:
    def __init__(self):
        """This class does not require an __init__ method and intentionally left empty."""
        pass

    @staticmethod
    def adapt(transactions_data: List[str, str, str]) -> Tuple[date, str, Decimal]:
        date_str, description, amount_str = transactions_data
        try:
            transaction_date = datetime.strptime(date_str, DATE_FORMAT).date()
        except ValueError:
            raise ValueError('wrong date format! Please use {DATE_FORMAT}')

        if transaction_date > date.today():
            raise ValueError('Transaction date is in the future!')

        if not description:
            raise ValueError('Missing transaction description!')

        try:
            transaction_amount = Decimal(amount_str).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
            if transaction_amount == 0:
                raise ValueError
        except ValueError:
            raise ValueError(f'Incorrect transaction amount!')

        return transaction_date, description, transaction_amount
