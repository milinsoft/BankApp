from datetime import date
from decimal import Decimal
from typing import List, Tuple

from app.models import TransactionData

from .fetchers import CSVTransactionsFetcher


class TransactionParser:
    """
    TransactionParser class for parsing transaction data from different file formats.

    This class uses the strategy pattern to dynamically select a parser based on the file format.

    Raises:
        ValueError: If the provided file format is not supported by any available parser.
    """

    # Define a mapping of file extensions to parser classes
    def __init__(self):
        """This class does not require an __init__ method and intentionally left empty."""
        pass

    STRATEGY_MAPPING = {'csv': CSVTransactionsFetcher}

    @classmethod
    def _get_strategy(cls, file_path) -> CSVTransactionsFetcher:
        return cls.STRATEGY_MAPPING.get(file_path.split('.')[-1])

    @classmethod
    def parse_data(cls, file_path: str) -> [TransactionData]:
        if not (parse_manager := cls._get_strategy(file_path)):
            raise ValueError(f'Unsupported file format.')
        return parse_manager.parse_file(file_path)
