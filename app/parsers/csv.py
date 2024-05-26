import csv

from app.parsers.parse_strategy import AbstractParseStrategy, check_description, parse_trx_amount
from app.schemas import STransactionAdd
from app.utils.helper_methods import date_from_string


# noinspection PyClassHasNoInit
class ParseCsv(AbstractParseStrategy):
    EXPECTED_HEADER = ["date", "description", "amount"]
    ROW_LENGTH = len(EXPECTED_HEADER)

    @classmethod
    def parse_data(cls, file_path: str, account_id: int) -> list[STransactionAdd]:
        with open(file_path, encoding="UTF-8-SIG") as f:
            csv_reader = csv.reader(f)
            cls._validate_header(next(csv_reader))  # Validate and skip the header row
            parsed_data = []
            for row_number, row in enumerate(csv_reader, start=1):
                try:
                    parsed_data.append(cls._process_row(row, account_id))
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
    def _process_row(cls, row: list[str], account_id: int) -> STransactionAdd:
        if row_len := len(row) != cls.ROW_LENGTH:
            raise ValueError(f"Incorrect number of elements. Expected: {cls.ROW_LENGTH} Found:{row_len}.")
        date_str, description, amount_str = row
        check_description(description)
        trx_date = date_from_string(date_str)
        trx_amount = parse_trx_amount(amount_str)

        return STransactionAdd(
            date=trx_date,
            amount=trx_amount,
            description=description,
            account_id=account_id,
        )
