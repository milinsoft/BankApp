from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, relationship  # type: ignore[attr-defined]

from app.domain_classes import AccountType
from app.schemas import AccountSchema, TransactionSchema

DEBIT = AccountType.DEBIT.value
CREDIT = AccountType.CREDIT.value


class Base(DeclarativeBase):
    ...


class Account(Base):
    # TODO: update syntax  to 2.0 version for models
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    account_type = Column(Integer, nullable=False)
    credit_limit = Column(Numeric(10, 2), default=0, comment="only for credit accounts")
    balance = Column(Numeric(10, 2), default=0)

    __table_args__ = (
        CheckConstraint(
            f"""(account_type = '{DEBIT}' AND credit_limit = 0 AND balance >= 0) OR
(account_type = '{CREDIT}' AND credit_limit < 0 AND balance >= credit_limit)""",
            name="Balance and credit limit constraints",
        ),
    )

    def to_read_model(self) -> AccountSchema:
        return AccountSchema(
            id=self.id,
            name=self.name,
            account_type=self.account_type,
            credit_limit=self.credit_limit,
            balance=self.balance,
        )


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    account = relationship("Account", backref="Transaction", order_by=date)  # type: ignore[var-annotated]

    def to_read_model(self) -> TransactionSchema:
        return TransactionSchema(
            id=self.id,
            date=self.date,
            description=self.description,
            amount=self.amount,
            account_id=self.account_id,
        )
