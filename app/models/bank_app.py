from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Annotated

AccountID = Annotated[int, "Bank Account ID"]

if TYPE_CHECKING:
    from app.database import Database
    from app.parsers import TransactionParser
    from app.schemas import STransaction
    from app.services import AccountService, TransactionService
    from app.utils import AbstractUnitOfWork


class BankApp(ABC):
    acc_service: "AccountService"
    trx_service: "TransactionService"
    db: "Database"
    account_id: AccountID
    uow: "AbstractUnitOfWork"
    parser: "TransactionParser"

    @abstractmethod
    def main_menu(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_balance(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def search_transactions(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def pick_account(self) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _get_transaction_table(cls, transactions: list["STransaction"]) -> str:
        raise NotImplementedError
