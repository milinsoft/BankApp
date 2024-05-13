import csv

from app.domain_classes import TransactionData
from app.parsers.parse_strategy import (
    AbstractParseStrategy,
    check_description,
    convert_str_to_date,
    convert_str_to_decimal_amount,
)


# noinspection PyClassHasNoInit
class ParseCsv(AbstractParseStrategy):
    EXPECTED_HEADER = ["date", "description", "amount"]
    ROW_LENGTH = len(EXPECTED_HEADER)

    @classmethod
    def parse_data(cls, file_path: str) -> list[TransactionData]:
        with open(file_path, encoding="UTF-8-SIG") as f:
            csv_reader = csv.reader(f)
            cls._validate_header(next(csv_reader))  # Validate and skip the header row
            parsed_data = []
            for row_number, row in enumerate(csv_reader, start=1):
                try:
                    parsed_data.append(cls._process_row(row))
                except ValueError as err:
                    raise ValueError(f"The row number {row_number}: {err}")
            if not parsed_data:
                raise ValueError("No data to import!")
        return parsed_data

    @classmethod
    def _validate_header(cls, header):
        if [col_name.lower().strip() for col_name in header] != cls.EXPECTED_HEADER:
            expected_header = ",".join(cls.EXPECTED_HEADER)
            raise ValueError(f"Incorrect header! Expected: {expected_header}")

    @classmethod
    def _process_row(cls, row: list[str]) -> TransactionData:
        if row_len := len(row) != cls.ROW_LENGTH:
            raise ValueError(f"Incorrect number of elements. Expected: {cls.ROW_LENGTH} Found:{row_len}.")
        date_str, description, amount_str = row
        check_description(description)
        trx_date = convert_str_to_date(date_str)
        trx_amount = convert_str_to_decimal_amount(amount_str)
        return TransactionData(trx_date, trx_amount, description)
