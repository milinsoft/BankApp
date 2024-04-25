from dataclasses import asdict
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import and_, desc

if TYPE_CHECKING:
    from app.domain_classes import TransactionData
    from app.schemas import TransactionSchema
    from app.utils import AbstractUnitOfWork


class TransactionService:
    @classmethod
    def get_by_date_range(
        cls, uow: "AbstractUnitOfWork", account_id: int, start_date: date | None = None, end_date: date | None = None
    ) -> list["TransactionSchema"]:
        start_date = start_date or datetime.min.date()
        end_date = end_date or date.today()
        with uow:
            trx = uow.transactions.model
            res = uow.transactions.get_all(
                filters=[and_(trx.date.between(start_date, end_date), trx.account_id == account_id)],
                order_by=desc(trx.date),
            )
            return res  # type: ignore[return-value]

    @classmethod
    def create(
        cls, uow: "AbstractUnitOfWork", account_id: int, data: list["TransactionData"]
    ) -> tuple[list[int], "Decimal"]:
        amount_to_add = Decimal(0)
        data_dicts = []
        for trx_data in data:
            data_dicts.append(asdict(trx_data.set_account_id(account_id)))
            amount_to_add += trx_data.amount
        with uow:  # single transaction
            transactions = uow.transactions.create_multi(data_dicts)
            new_balance = uow.account.update_balance(account_id=account_id, amount_to_add=amount_to_add)
            uow.commit()
            return transactions, new_balance
