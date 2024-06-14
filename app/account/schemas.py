from decimal import Decimal

from pydantic import PositiveInt

from app.schemas import ModelSchema


class SAccountAdd(ModelSchema):
    name: str
    account_type: PositiveInt
    credit_limit: Decimal
    balance: Decimal


class SAccount(SAccountAdd):
    id: PositiveInt
