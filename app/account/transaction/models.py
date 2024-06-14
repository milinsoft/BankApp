from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from ..type_annotations import col_num_10_2

if TYPE_CHECKING:
    from ..models import Account


class Transaction(Base):
    __tablename__ = "transaction"

    date: Mapped[date] = mapped_column(Date)
    description: Mapped[str]
    amount: Mapped[col_num_10_2]
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship(back_populates="transactions", order_by=date)
