from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Tuple

from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import declarative_base, relationship, validates

Base = declarative_base()


@dataclass
class TransactionData:
    date: date
    description: str
    amount: Decimal


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    account = relationship('Account', backref='Transaction')


class AccountType(Enum):
    CREDIT = 'Credit'
    DEBIT = 'Debit'


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    credit_limit = Column(Numeric(10, 2), default=0)  # only for Credit accounts
    balance = Column(Numeric(10, 2), default=0)

    __table_args__ = (
        CheckConstraint(
            f"(account_type = '{AccountType.DEBIT.value}' AND credit_limit = 0 AND balance >= 0) OR "
            f"(account_type = '{AccountType.CREDIT.value}' AND credit_limit < 0 AND balance >= credit_limit)",
            name='Balance and credit limit constraints',
        ),
    )

    def get_balance_on_date(self, trx_date: Optional[date] = None) -> int | float:
        today_date = date.today()
        trx_date = trx_date or today_date
        assert trx_date <= today_date, 'You cannot lookup in the future! :)'

        transactions_prior_date = self.get_range_transactions(end_date=trx_date)
        return sum((t.amount for t in transactions_prior_date))

    def get_range_transactions(self, start_date: date = None, end_date: date = None) -> List[Transaction]:
        if not start_date and not end_date:
            return self.Transaction

        start_date = start_date or datetime.min.date()
        end_date = end_date or date.today()

        return sorted([t for t in self.Transaction if start_date <= t.date <= end_date], key=lambda _t: _t.date)

    # interface
    def create_transactions(self, transactions_data: List[TransactionData]) -> List[Transaction]:
        """create transactions without saving"""
        new_balance = self.balance + sum(_t.amount for _t in transactions_data)
        if new_balance < self.credit_limit:
            raise ValueError(
                f'\nImpossible to import data, as your account balance would go less than {self.credit_limit}'
            )

        # update balance
        self.balance = new_balance

        return [
            Transaction(date=_t.date, description=_t.description, amount=_t.amount, account_id=self.id)
            for _t in transactions_data
        ]
