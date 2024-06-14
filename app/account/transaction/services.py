from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Annotated

from pydantic import PositiveInt, TypeAdapter
from sqlalchemy import and_, desc

from .type_annotations import TransactionsDataList, TransactionsList

if TYPE_CHECKING:
    from app.uow import AbstractUoW

IDs = Annotated[list[PositiveInt], "IDs"]
trx_adapter = TypeAdapter(TransactionsList)


class TransactionService:
    @classmethod
    def get_by_date_range(
        cls,
        uow: "AbstractUoW",
        account_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> TransactionsList:
        start_date = start_date or datetime.min.date()
        end_date = end_date or date.today()
        with (uow):
            trx = uow.transactions.model
            transactions = uow.transactions.get_all(
                filters=[
                    and_(
                        trx.date.between(start_date, end_date),
                        trx.account_id == account_id,
                    )
                ],
                order_by=desc(trx.date),
            )
            if not transactions:
                return []
            return trx_adapter.validate_python(transactions)

    @classmethod
    def create(cls, uow: "AbstractUoW", account_id: int, data: TransactionsDataList) -> IDs:
        with uow:  # single transaction
            transactions = uow.transactions.create_multi(data_list=[d.model_dump() for d in data])
            uow.account.update_balance(account_id, Decimal(sum(trx.amount for trx in data)))
            return transactions
