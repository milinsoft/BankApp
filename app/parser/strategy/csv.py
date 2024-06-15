import csv
from typing import Annotated

from _collections_abc import Sequence

from app.account.transaction.schemas import STransactionAdd

Transactions = Annotated[list[STransactionAdd], "Transactions"]
CsvHeader = Annotated[Sequence[str] | None, "CSV Header"]
CsvRow = Annotated[dict[str, str], "CSV Row"]


# noinspection PyClassHasNoInit
class CsvStrategy:
    EXPECTED_HEADER = ["date", "description", "amount"]
    ROW_LENGTH = len(EXPECTED_HEADER)

    @classmethod
    def parse_data(cls, file_path: str, account_id: int) -> Transactions:
        with open(file_path, encoding="UTF-8") as f:
            csv_reader = csv.DictReader(f)
            cls._validate_header(csv_reader.fieldnames)
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
    def _validate_header(cls, header: CsvHeader) -> None:
        if header != cls.EXPECTED_HEADER:
            raise ValueError(f"Incorrect header! Expected: {cls.EXPECTED_HEADER}")

    @classmethod
    def _process_row(cls, row: CsvRow, account_id: int) -> STransactionAdd:
        if row_len := len(row.values()) != cls.ROW_LENGTH:
            raise ValueError(f"Incorrect number of elements. Expected: {cls.ROW_LENGTH} Found:{row_len}.")
        return STransactionAdd(**row, account_id=account_id)
