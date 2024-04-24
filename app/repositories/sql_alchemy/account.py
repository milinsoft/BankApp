from datetime import date
from typing import TYPE_CHECKING, Union

from app import repositories
from app.models.account import Account

from .transaction import TransactionRepository

if TYPE_CHECKING:
    from decimal import Decimal

    from sqlalchemy.orm import Session


class AccountRepository(repositories.AccountRepository):
    def __init__(self, session: "Session"):
        self.session: "Session" = session
        self.query = self.session.query(Account)

    def create(self, **kwargs) -> list[Account]:
        new_account = Account(**kwargs)
        self.session.add(new_account)
        self.session.commit()
        return new_account

    def get_by_type(self, account_type: str):
        return self.query.filter_by(account_type=account_type).first()

    def get_all(self) -> list[Account]:
        return self.query.all()

    def get_by_id(self, account_id: int) -> Account | None:
        return self.query.filter(Account.id == account_id).first()

    def get_balance(self, account: Account, trx_date: date | None = None) -> Union[int, "Decimal"]:
        if not trx_date:
            return account.balance  # type: ignore
            # Incompatible return value type (got "Column[Decimal]", expected "int | Decimal")
        if trx_date > date.today():
            raise ValueError("You cannot lookup in the future! :)")
        transactions = TransactionRepository(self.session).get_by_date_range(account, end_date=trx_date)
        return sum(t.amount for t in transactions)  # type: ignore
        # Generator has incompatible item type "Column[Decimal]"; expected "bool"
