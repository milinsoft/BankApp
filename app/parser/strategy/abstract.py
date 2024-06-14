from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from app.account.transaction.type_annotations import TransactionsDataList


class Strategy(Protocol):
    @classmethod
    def parse_data(cls, file_path: str, account_id: int) -> "TransactionsDataList":
        raise NotImplementedError
