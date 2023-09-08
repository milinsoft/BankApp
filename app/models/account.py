from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Column, Integer, Numeric, String

from .base import Base
from .orm_independent import AccountType

if TYPE_CHECKING:
    pass


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    account_type = Column(Integer, nullable=False)
    credit_limit = Column(Numeric(10, 2), default=0, comment="only for credit accounts")
    balance = Column(Numeric(10, 2), default=0)

    __table_args__ = (
        CheckConstraint(
            f"(account_type = '{AccountType.DEBIT.value}' AND credit_limit = 0 AND balance >= 0) OR "
            f"(account_type = '{AccountType.CREDIT.value}' AND credit_limit < 0 AND balance >= credit_limit)",
            name="Balance and credit limit constraints",
        ),
    )
