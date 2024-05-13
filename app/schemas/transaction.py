from datetime import date
from decimal import Decimal

from pydantic import BaseModel, PositiveInt


class TransactionSchema(BaseModel):
    id: PositiveInt
    date: date
    description: str
    amount: Decimal
    account_id: PositiveInt

    class Config:  # noqa: D105,D106
        from_attributes = True
