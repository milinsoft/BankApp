from datetime import date, datetime
from logging import getLogger
from os.path import exists
from typing import TYPE_CHECKING

from app.account import AccountType
from app.account.services import AccountService
from app.account.transaction.services import TransactionService
from app.config import settings
from app.database import Database
from app.parser import TransactionParser
from app.utils.uow import UoW

if TYPE_CHECKING:
    from app.account.transaction.type_annotations import TransactionsList
    from app.utils.uow import AbstractUoW


_logger = getLogger(__name__)


class BankAppCli:
    def __init__(self, db: Database) -> None:
        self.acc_service: "AccountService" = AccountService()
        self.trx_service: "TransactionService" = TransactionService()
        self.db: "Database" = db
        self.account_id: int
        self.uow: "AbstractUoW" = UoW(db)  # imported instance
        self.parser: "TransactionParser" = TransactionParser()

        self.menu_options = {
            "0": ("Exit", self.exit_app),
            "1": ("Import transactions (supported formats are: csv)", self.import_data),
            "2": ("Show balance", self.show_balance),
            "3": ("Search transactions for the a given period", self.search_transactions),
        }
        self.menu_msg = "\n".join(f"{k}: {v[0]}" for k, v in self.menu_options.items())

    def main_menu(self) -> None:
        self.pick_account()
        while True:
            choice = self.get_valid_action()
            action = self.menu_options[choice][1]
            action()

    def import_data(self):
        try:
            trx_data = self.parser.parse_data(self.get_file_path(), account_id=self.account_id)
            _, balance = self.trx_service.create(self.uow, self.account_id, trx_data)
            print(f"Transactions have been loaded successfully! Current balance: {balance}")
        except ValueError as e:
            _logger.error(e)

    @classmethod
    def get_file_path(cls) -> str:
        while True:
            file_path = input("Please provide the path to your file: ").strip("'\"")
            if not exists(file_path):
                print("Incorrect file path, please try again!")
            else:
                return file_path

    def show_balance(self):
        _date = self._get_date(mode="end_date")
        print(
            f"Your balance on {_date} is: ",
            self.acc_service.get_balance(self.uow, self.account_id, _date),
        )

    def _search_transactions(self) -> "TransactionsList":
        return self.trx_service.get_by_date_range(
            self.uow, self.account_id, self._get_date("start_date"), self._get_date("end_date")
        )

    def search_transactions(self) -> None:
        transactions = self._search_transactions()
        print(self._get_transaction_table(transactions) if transactions else "No transactions found!")

    def get_valid_action(self):
        print("\nPICK AN OPTION: ")
        action = False
        while action not in self.menu_options.keys():
            action = input(f"{self.menu_msg}\n").strip()
        return action

    @staticmethod
    def _get_date(mode: str):
        if mode not in (allowed_modes := ("start_date", "end_date")):
            raise ValueError(f"Invalid mode: {mode}. Allowed modes are {allowed_modes}")
        today_date = date.today()

        def compose__get_date_message() -> str:
            date_example = datetime.strftime(today_date, settings.DATE_FORMAT)
            action_description = (
                "search from the oldest transaction\n"
                if mode == allowed_modes[0]
                else "pick today's date by default!\n"
            )
            return (
                f"\nProvide the {mode} in the following {date_example} format or "
                f"{action_description}\n press enter/return to {action_description}"
            )

        msg = compose__get_date_message()
        while True:
            _date: str | date = input(msg).strip()
            if not _date:
                return datetime.min.date() if mode == allowed_modes[0] else today_date
            try:
                _date = datetime.strptime(_date, settings.DATE_FORMAT).date()  # type: ignore[arg-type]
            except ValueError:
                _logger.error("Incorrect data format")
            else:
                if _date > today_date:
                    _date = today_date
                return _date

    @staticmethod
    def _get_account_type() -> AccountType:
        acc_type = None
        while not acc_type:
            acc_type = getattr(
                AccountType, input("Pick an account: Debit or Credit (debit/credit): ").upper().strip(), ""
            )
        return acc_type

    def pick_account(self) -> None:
        acc_type = self._get_account_type()
        existing_account = self.acc_service.get_by_type(self.uow, acc_type)
        self.account_id = existing_account.id if existing_account else self.acc_service.create_one(self.uow, acc_type)

    @classmethod
    def _get_transaction_table(cls, transactions: "TransactionsList") -> str:
        """Return transactions in a tabular str format."""
        from tabulate import tabulate

        return tabulate(
            [(t.date, t.description, t.amount) for t in transactions],
            headers=["Date", "Description", "Amount"],
            colalign=("left", "left", "right"),
            tablefmt="pretty",
        )

    @staticmethod
    def exit_app():
        exit(print("Goodbye!"))
