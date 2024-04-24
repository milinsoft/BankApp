from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


@dataclass
class TransactionData:
    date: date
    amount: Decimal
    description: str


class AccountType(Enum):
    CREDIT = 1
    DEBIT = 2
