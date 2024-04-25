from typing import TYPE_CHECKING

from app.parsers.csv import ParseCsv

if TYPE_CHECKING:
    from app.domain_classes import TransactionData

    from .csv import AbstractParseStrategy


class TransactionParser:
    """TransactionParser class for parsing transaction data from different file formats.

    This class uses the strategy pattern to dynamically select a parser based on the file format.

    Raises:
        ValueError: If the provided file format is not supported by any available parser.

    """

    strategy_map = {"csv": ParseCsv}

    def _get_strategy(self, file_path: str) -> type["AbstractParseStrategy"] | None:
        return self.strategy_map.get(file_path.split(".")[-1].lower())

    def parse_data(self, file_path: str) -> list["TransactionData"]:
        if not (parser := self._get_strategy(file_path)):
            raise ValueError("Unsupported file format.")
        data = parser.parse_data(file_path)
        return data
