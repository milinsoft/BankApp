from decimal import Decimal

from pydantic import BaseModel, PositiveInt


class AccountSchema(BaseModel):
    id: PositiveInt
    name: str
    account_type: PositiveInt
    credit_limit: Decimal
    balance: Decimal

    class Config:  # noqa: D105,D106
        from_attributes = True
