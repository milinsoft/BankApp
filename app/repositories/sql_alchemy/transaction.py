from collections.abc import Sequence
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import desc
from sqlalchemy.sql.expression import and_

from app import repositories
from app.models.account import Account
from app.models.transaction import Transaction

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from app.models import TransactionData


class TransactionRepository(repositories.TransactionRepository):
    def __init__(self, session: "Session"):
        self.session: "Session" = session
        self.query = self.session.query(Transaction)

    def create(self, account: "Account", data: Sequence["TransactionData"]) -> list[Transaction]:
        new_balance = account.balance + sum(_t.amount for _t in data)
        if new_balance < account.credit_limit:
            raise ValueError(
                f"\nImpossible to import data, as your account balance would go less than {account.credit_limit}"
            )
        new_transactions = [
            Transaction(
                date=_t.date,
                description=_t.description,
                amount=_t.amount,
                account_id=account.id,
            )
            for _t in data
        ]
        # account.balance = new_balance
        self.session.add_all(new_transactions)
        self.session.commit()
        account.balance = new_balance  # type: ignore
        # expression has type "ColumnElement[Decimal]", variable has type "Column[Decimal]"
        return new_transactions

    def get_by_account(self, account_id: str):
        return self.query.filter_by(account_id=account_id).all()

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        return self.query.filter(Transaction.id == transaction_id).first()

    def get_all(self) -> list[Transaction]:
        return self.query.all()

    def get_by_date_range(
        self, account: "Account", start_date: date | None = None, end_date: date | None = None
    ) -> list["Transaction"]:
        start_date = start_date or datetime.min.date()
        end_date = end_date or date.today()
        # Splitting filters for better readability
        date_filter = Transaction.date.between(start_date, end_date)
        account_filter = Transaction.account_id == account.id

        query = self.query.filter(and_(date_filter, account_filter))
        query = query.order_by(desc(Transaction.date))
        return query.all()
