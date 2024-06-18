from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import func

from app.account import Account, AccountType, Transaction
from app.account.schemas import SAccount, SAccountAdd
from app.config import settings

if TYPE_CHECKING:
    from app.utils.uow import AbstractUoW


class AccountService:
    @classmethod
    def get_balance(cls, uow: "AbstractUoW", account_id: int, trx_date: date | None = None) -> "Decimal":
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
        uow: "AbstractUoW",
        acc_type: "AccountType",
        data: SAccountAdd | None = None,
    ) -> int:
        data = data or cls._get_default_schema(acc_type)
        with uow:
            return uow.account.create_one(data.model_dump())

    @classmethod
    def get_one(cls, uow: "AbstractUoW", filters=None, order_by=None) -> SAccount | None:
        with uow:
            account = uow.account.get_one(filters, order_by)
            return account and SAccount.model_validate(account) or None

    def get_by_type(self, uow: "AbstractUoW", account_type: "AccountType") -> SAccount | None:
        return self.get_one(uow, filters=[Account.account_type == account_type])

    @classmethod
    def get_by_id(cls, uow: "AbstractUoW", rec_id: int) -> SAccount | None:
        with uow:
            account = uow.account.get_by_id(rec_id)
            return account and SAccount.model_validate(account) or None

    @staticmethod
    def _get_default_schema(account_type: AccountType) -> SAccountAdd:
        """Add default values for debit account."""
        return SAccountAdd(
            name=f"{account_type.name.capitalize()} Account",
            account_type=account_type,
            credit_limit=0 if account_type == AccountType.DEBIT else settings.DEFAULT_CREDIT_LIMIT,
            balance=0,
        )
