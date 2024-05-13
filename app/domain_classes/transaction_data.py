from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class TransactionData:
    date: date | str
    amount: Decimal
    description: str
    account_id: int | None = None

    def set_account_id(self, account_id: int) -> "TransactionData":
        self.account_id = account_id
        return self
