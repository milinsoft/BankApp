from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.repositories import AccountRepository, TransactionRepository

if TYPE_CHECKING:
    from app.database import Database


class AbstractUnitOfWork(ABC):
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

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, database: "Database") -> None:
        self.database = database

    def __enter__(self) -> None:  # noqa: D105
        self.session = self.database.create_session()
        self.account = AccountRepository(self.session)
        self.transactions = TransactionRepository(self.session)

    def __exit__(self, *args) -> None:  # noqa: D105
        self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
