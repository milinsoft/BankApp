from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from app.database import Base

from .type_annotations import col_num_10_2

if TYPE_CHECKING:
    from .transaction import Transaction


class AccountType(int, Enum):
    CREDIT: int = 1
    DEBIT: int = 2


class Account(Base):
    __tablename__ = "account"

    name: Mapped[str]
    account_type: Mapped[int]
    credit_limit: Mapped[col_num_10_2] = mapped_column(comment="only for credit accounts")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account")
    balance: Mapped[col_num_10_2]

    __table_args__ = (
        CheckConstraint(
            f"""(account_type = '{AccountType.DEBIT.value}' AND credit_limit = 0 AND balance >= 0) OR
(account_type = '{AccountType.CREDIT.value}' AND credit_limit < 0 AND balance >= credit_limit)""",
            name="Balance and credit limit constraints",
        ),
    )
