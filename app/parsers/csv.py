import csv
from collections.abc import Sequence

from app.models.orm_independent import TransactionData
from app.parsers.base import ParseStrategy


# noinspection PyClassHasNoInit
class ParseCsv(ParseStrategy):
    EXPECTED_HEADER = ["date", "description", "amount"]
    ROW_LENGTH = 3

    @classmethod
    def parse_data(cls, file_path: str) -> Sequence[TransactionData]:
        parsed_data = []
        with open(file_path, encoding="UTF-8-SIG") as f:
            csv_reader = csv.reader(f)
            cls._validate_header(next(csv_reader))  # Validate and skip the header row
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
            msg = "Incorrect header! Expected: " + ",".join(cls.EXPECTED_HEADER)
            raise ValueError(msg)

    @classmethod
    def _process_row(cls, row: Sequence[str]) -> TransactionData:
        if row_len := len(row) != cls.ROW_LENGTH:
            raise ValueError(f"Incorrect number of elements. Expected: {cls.ROW_LENGTH} Found:{row_len}.")
        date_str, description, amount_str = row
        cls._check_description(description)
        return TransactionData(cls._convert_date(date_str), cls._convert_amount(amount_str), description)
