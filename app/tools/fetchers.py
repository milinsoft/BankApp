import csv
from datetime import date
from decimal import Decimal
from typing import List, Tuple

from .adapters import TransactionsAdapter


class CSVTransactionsFetcher:
    def __init__(self):
        """This class does not require an __init__ method and intentionally left empty."""
        pass

    ROW_LENGTH = 3  # Number of elements expected in each row

    @classmethod
    def parse_file(cls, file_path: str) -> List[Tuple[date, str, Decimal]]:
        parsed_data = []

        with open(file_path, 'r', encoding='UTF-8-SIG') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip the header row

            for row_number, row in enumerate(csv_reader, start=1):
                if len(row) != cls.ROW_LENGTH:
                    raise ValueError(f'Row number {row_number} has {len(row)} elements, expected {cls.ROW_LENGTH}')

                try:
                    adapted_data = TransactionsAdapter.adapt(row)

                except ValueError as err:
                    print(f'Row number {row_number}: {err}')

                parsed_data.append(adapted_data)
        return parsed_data
