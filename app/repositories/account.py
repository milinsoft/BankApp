from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from datetime import date
    from decimal import Decimal

    from app.models import Account


class AccountRepository(ABC):
    @abstractmethod
    def create(self, **kwargs) -> list["Account"]:
        pass

    @abstractmethod
    def get_by_type(self, account_type: str):
        pass

    @abstractmethod
    def get_all(self) -> list["Account"]:
        pass

    @abstractmethod
    def get_by_id(self, account_id: int) -> Optional["Account"]:
        pass

    @abstractmethod
    def get_balance(self, account: "Account", trx_date: Optional["date"] = None) -> Union[int, "Decimal"]:
        pass
