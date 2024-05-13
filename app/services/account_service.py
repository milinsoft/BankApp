from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import func

import settings
from app.domain_classes import AccountType
from app.models import Account, Transaction
from app.schemas import AccountSchema

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
                filters=[Transaction.date <= trx_date, Transaction.account_id == account_id],
                aggregate_func=func.sum,
                column_name="amount",
            )
            balance = result[0] or 0
            return Decimal(balance)

    @classmethod
    def create_one(cls, uow: "AbstractUnitOfWork", acc_type: "AccountType", data: dict | None = None) -> int:
        data = data or {}
        cls._add_defaults(data, acc_type)
        with uow:
            account = uow.account.create_one(data)
            uow.commit()
            return account

    @classmethod
    def get_one(cls, uow: "AbstractUnitOfWork", filters=None, order_by=None) -> "AccountSchema":
        with uow:
            return uow.account.get_one(filters, order_by)  # type: ignore[return-value]

    def get_by_type(self, uow: "AbstractUnitOfWork", account_type: "AccountType") -> "AccountSchema":
        return self.get_one(uow, filters=[Account.account_type == account_type.value])

    @classmethod
    def get_by_id(cls, uow: "AbstractUnitOfWork", rec_id: int) -> "AccountSchema":
        with uow:
            return uow.account.get_by_id(rec_id)  # type: ignore[return-value]

    @staticmethod
    def _add_defaults(params: dict, account_type: AccountType) -> None:
        """Add default values for debit account."""
        params.setdefault("name", f"{account_type.name.capitalize()} Account")
        params.setdefault("account_type", account_type.value)
        if account_type == AccountType.CREDIT:
            params.setdefault("credit_limit", settings.DEFAULT_CREDIT_LIMIT)
