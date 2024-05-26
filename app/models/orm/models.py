from datetime import date
from typing import Annotated

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from app.schemas import SAccount, STransaction

from ..account_type import AccountType

DEBIT = AccountType.DEBIT.value
CREDIT = AccountType.CREDIT.value
col_num_10_2 = Annotated[float, mapped_column(Numeric(10, 2), default=0)]


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Account(Base):
    __tablename__ = "account"

    name: Mapped[str]
    account_type: Mapped[int]
    credit_limit: Mapped[col_num_10_2] = mapped_column(comment="only for credit accounts")
    balance: Mapped[col_num_10_2]

    __table_args__ = (
        CheckConstraint(
            f"""(account_type = '{DEBIT}' AND credit_limit = 0 AND balance >= 0) OR
(account_type = '{CREDIT}' AND credit_limit < 0 AND balance >= credit_limit)""",
            name="Balance and credit limit constraints",
        ),
    )

    def to_read_model(self) -> SAccount:
        return SAccount(
            id=self.id,
            name=self.name,
            account_type=self.account_type,
            credit_limit=self.credit_limit,
            balance=self.balance,
        )


class Transaction(Base):
    __tablename__ = "transaction"

    date: Mapped[date] = mapped_column(Date)
    description: Mapped[str]
    amount: Mapped[col_num_10_2]
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    account = relationship("Account", backref="Transaction", order_by=date)  # type: ignore[var-annotated]

    def to_read_model(self) -> STransaction:
        return STransaction(
            id=self.id,
            date=self.date,
            description=self.description,
            amount=self.amount,
            account_id=self.account_id,
        )
