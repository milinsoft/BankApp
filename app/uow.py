from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.account import AccountRepository, TransactionRepository

if TYPE_CHECKING:
    from app.database import Database


class AbstractUoW(ABC):
    acc_rep: type[AccountRepository]
    trx_rep: type[TransactionRepository]  # Type as class is accepted, not instance
    account: AccountRepository
    transactions: TransactionRepository

    @abstractmethod
    def __enter__(self):  # noqa: D105
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, *args):  # noqa: D105
        raise NotImplementedError


class UoW(AbstractUoW):
    def __init__(self, database: "Database") -> None:
        self.database = database

    def __enter__(self) -> None:  # noqa: D105
        self.session = self.database.create_session()
        self.account = AccountRepository(self.session)
        self.transactions = TransactionRepository(self.session)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: D105
        if exc_type:
            self.session.rollback()
        self.session.commit()
        self.session.close()
