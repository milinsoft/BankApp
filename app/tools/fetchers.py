import csv
from datetime import date
from decimal import Decimal
from typing import List, Tuple

from app.models import TransactionData
from settings import CSV_ROW_LENGTH

from .adapters import TransactionsAdapter


class CSVTransactionsFetcher:
    EXPECTED_HEADER = ['date', 'description', 'amount']

    def __init__(self):
        """This class does not require an __init__ method and intentionally left empty."""
        pass

    @classmethod
    def parse_file(cls, file_path: str) -> [TransactionData]:
        parsed_data = []

        with open(file_path, 'r', encoding='UTF-8-SIG') as f:
            csv_reader = csv.reader(f)
            header = next(csv_reader)  # Skip the header row
            cls._validate_header(header)

            for row_number, row in enumerate(csv_reader, start=1):
                if len(row) != CSV_ROW_LENGTH:
                    raise ValueError(f'Row number {row_number} has {len(row)} elements, expected {CSV_ROW_LENGTH}')

                try:
                    adapted_data = TransactionsAdapter.adapt(row)
                    parsed_data.append(adapted_data)

                except ValueError as err:
                    raise ValueError(f'Row number {row_number}: {err}')
        if not parsed_data:
            raise ValueError('No data to import!')
        return parsed_data

    @classmethod
    def _validate_header(cls, header):
        if [col_name.lower().strip() for col_name in header] != cls.EXPECTED_HEADER:
            msg = 'Incorrect header! Expected: ' + ','.join(cls.EXPECTED_HEADER)
            raise ValueError(msg)
