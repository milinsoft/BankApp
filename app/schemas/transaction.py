from datetime import date
from decimal import Decimal

from pydantic import PositiveInt

from .model_schema import ModelSchema


class STransactionAdd(ModelSchema):
    date: date
    amount: Decimal
    description: str
    account_id: PositiveInt


class STransaction(STransactionAdd):
    id: PositiveInt
