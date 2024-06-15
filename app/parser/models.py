from typing import TYPE_CHECKING

from .strategy import CsvStrategy, Strategy

if TYPE_CHECKING:
    from app.account.transaction.type_annotations import TransactionsDataList

strategy_map = {"csv": CsvStrategy}


class TransactionParser:
    """TransactionParser class for parsing transaction data from different file formats.

    Utilizes strategy pattern to dynamically select a parser based on the file format.

    Raises:
        ValueError: If the provided file format is not supported.

    """

    @staticmethod
    def _get_strategy(file_path: str) -> type[Strategy]:
        file_ext = file_path.split(".")[-1].lower()
        if not (parser := strategy_map.get(file_ext)):
            raise ValueError("Unsupported file format.")
        return parser

    @classmethod
    def parse_data(cls, file_path: str, account_id: int) -> "TransactionsDataList":
        parse_strategy = cls._get_strategy(file_path)
        return parse_strategy.parse_data(file_path, account_id)
