from collections.abc import Sequence
from typing import TYPE_CHECKING

from app.parsers.csv import ParseCsv

if TYPE_CHECKING:
    from app.models import Account, TransactionData

    from .csv import ParseStrategy


class TransactionParser:
    """TransactionParser class for parsing transaction data from different file formats.

    This class uses the strategy pattern to dynamically select a parser based on the file format.

    Raises:
        ValueError: If the provided file format is not supported by any available parser.

    """

    strategy_map = {"csv": ParseCsv}

    def __init__(self, session, transaction_repository):
        self.session = session
        self.transaction_repository = transaction_repository

    def _get_strategy(self, file_path: str) -> type["ParseStrategy"] | None:
        return self.strategy_map.get(file_path.split(".")[-1].lower())

    def parse_data(self, file_path: str, current_account: "Account") -> Sequence["TransactionData"]:
        if not (parser := self._get_strategy(file_path)):
            raise ValueError("Unsupported file format.")
        data = parser.parse_data(file_path)
        self._save_to_db(current_account, data)
        return data

    def _save_to_db(self, current_account, transaction_data: Sequence["TransactionData"]):
        self.session.add_all(self.transaction_repository.create(current_account, transaction_data))
        self.session.commit()
