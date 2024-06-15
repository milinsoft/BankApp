from datetime import date
from decimal import Decimal, InvalidOperation

from pydantic import PositiveInt, field_validator

from app.schemas import ModelSchema
from app.utils.helper_methods import to_decimal


class STransactionAdd(ModelSchema):
    date: date
    amount: Decimal
    description: str
    account_id: PositiveInt

    @field_validator('amount')
    def validate_amount_not_zero(cls, amount):
        try:
            converted_amount = to_decimal(amount)
            if not converted_amount:
                raise ValueError
        except (ValueError, InvalidOperation):
            raise ValueError("Incorrect transaction amount!")
        return converted_amount

    @field_validator('description')
    def validate_description_is_not_empty(cls, description):
        if not description:
            raise ValueError("Missing transaction description!")
        return description


class STransaction(STransactionAdd):
    id: PositiveInt
