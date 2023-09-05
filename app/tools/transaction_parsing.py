import csv
from abc import ABC, abstractmethod
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import List

from app.models import Transaction, TransactionData
from settings import CSV_ROW_LENGTH, DATE_FORMAT


def adapt_transactions(transactions_data: List[str]) -> TransactionData:
    date_str, description, amount_str = transactions_data
    try:
        transaction_date = datetime.strptime(date_str, DATE_FORMAT).date()
    except ValueError:
        raise ValueError(f'wrong date format! Please use {DATE_FORMAT}')

    if transaction_date > date.today():
        raise ValueError('Transaction date is in the future!')

    if not description:
        raise ValueError('Missing transaction description!')

    try:
        transaction_amount = Decimal(amount_str).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        if transaction_amount == 0:
            raise ValueError
    except (ValueError, InvalidOperation):
        raise ValueError(f'Incorrect transaction amount!')

    return TransactionData(transaction_date, description, transaction_amount)


# noinspection PyClassHasNoInit
class CSVTransactionFetcher:
    EXPECTED_HEADER = ['date', 'description', 'amount']

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
                    adapted_data = adapt_transactions(row)
                except ValueError as err:
                    raise ValueError(f'Row number {row_number}: {err}')
                else:
                    parsed_data.append(adapted_data)
        if not parsed_data:
            raise ValueError('No data to import!')
        return parsed_data

    @classmethod
    def _validate_header(cls, header):
        if [col_name.lower().strip() for col_name in header] != cls.EXPECTED_HEADER:
            msg = "Incorrect header! Expected: " + ",".join(cls.EXPECTED_HEADER)
            raise ValueError(msg)


class TransactionParser:
    """
    TransactionParser class for parsing transaction data from different file formats.

    This class uses the strategy pattern to dynamically select a parser based on the file format.

    Raises:
        ValueError: If the provided file format is not supported by any available parser.
    """

    # Define a mapping of file extensions to parser classes
    STRATEGY_MAPPING = {"csv": CSVTransactionFetcher}

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.parse_data()

    def _get_strategy(self) -> CSVTransactionFetcher | None:
        return self.STRATEGY_MAPPING.get(self.file_path.split('.')[-1].lower())

    def parse_data(self) -> [TransactionData]:
        if not (parse_manager := self._get_strategy()):
            raise ValueError(f'Unsupported file format.')
        return parse_manager.parse_file(self.file_path)
