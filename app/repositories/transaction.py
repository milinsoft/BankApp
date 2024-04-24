from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from datetime import date

    from app.models import Account, Transaction, TransactionData


class TransactionRepository(ABC):
    @abstractmethod
    def create(self, account: "Account", data: Sequence["TransactionData"]) -> list["Transaction"]:
        pass

    @abstractmethod
    def get_by_account(self, account_id: str):
        pass

    @abstractmethod
    def get_by_id(self, transaction_id: int) -> Optional["Transaction"]:
        pass

    @abstractmethod
    def get_all(self) -> list["Transaction"]:
        pass

    @abstractmethod
    def get_by_date_range(
        self, account: "Account", start_date: Optional["date"] = None, end_date: Union["date", None] = None
    ) -> list["Transaction"]:
        pass
