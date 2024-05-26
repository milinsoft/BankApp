from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import func

import settings
from app.models import AccountType
from app.models.orm import Account, Transaction
from app.schemas import ModelSchema, SAccount, SAccountAdd

from .transaction_service import TransactionService

if TYPE_CHECKING:
    from app.utils import AbstractUnitOfWork


class AccountService:
    def __init__(self):
        self.trx_service = TransactionService()

    @classmethod
    def get_balance(cls, uow: "AbstractUnitOfWork", account_id: int, trx_date: date | None = None) -> "Decimal":
        if trx_date:
            if trx_date > date.today():
                raise ValueError("You cannot lookup in the future! :)")
        else:
            trx_date = date.today()
        with uow:
            result = uow.transactions.get_aggregated(
                filters=[
                    Transaction.date <= trx_date,
                    Transaction.account_id == account_id,
                ],
                aggregate_func=func.sum,
                column_name="amount",
            )
            balance = result[0] or 0
            return Decimal(balance)

    @classmethod
    def create_one(
        cls,
        uow: "AbstractUnitOfWork",
        acc_type: "AccountType",
        data: ModelSchema | None = None,
    ) -> int:
        data = data or cls._get_default_schema(acc_type)
        with uow:
            account = uow.account.create_one(data)
            uow.commit()
            return account

    @classmethod
    def get_one(cls, uow: "AbstractUnitOfWork", filters=None, order_by=None) -> "SAccount":
        with uow:
            return uow.account.get_one(filters, order_by)  # type: ignore[return-value]

    def get_by_type(self, uow: "AbstractUnitOfWork", account_type: "AccountType") -> "SAccount":
        return self.get_one(uow, filters=[Account.account_type == account_type.value])

    @classmethod
    def get_by_id(cls, uow: "AbstractUnitOfWork", rec_id: int) -> "SAccount":
        with uow:
            return uow.account.get_by_id(rec_id)  # type: ignore[return-value]

    @staticmethod
    def _get_default_schema(account_type: AccountType) -> SAccountAdd:
        """Add default values for debit account."""
        return SAccountAdd(
            name=f"{account_type.name.capitalize()} Account",
            account_type=account_type.value,
            credit_limit=0 if account_type == AccountType.DEBIT else settings.DEFAULT_CREDIT_LIMIT,
            balance=0,
        )
