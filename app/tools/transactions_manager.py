from datetime import date
from decimal import Decimal
from typing import List, Tuple

from sqlalchemy.exc import SQLAlchemyError
from tabulate import tabulate

from app.models import Account, Transaction
from app.tools import TransactionParser


class TransactionsManager:
    def __init__(self, session, current_account: Account):
        self.session = session
        self.current_account = current_account

    def import_data(self, file_path: str):
        transactions_data = TransactionParser.parse_data(file_path)
        self._save_to_db(transactions_data)

    def _save_to_db(self, transactions_data):
        try:
            with self.session.begin_nested():
                transactions = self.current_account.create_transactions(transactions_data)
                self.session.add_all(transactions)
        except SQLAlchemyError as err:
            raise err
        self.session.commit()

    def _update_account_balance(self, transactions_data):
        self.current_account.balance += sum(row[2] for row in transactions_data)

    def search_transactions(self, start_date: date, end_date: date) -> List['Transaction']:
        return self.current_account.get_range_transactions(start_date, end_date)

    @staticmethod
    def display_transactions(transactions: List['Transaction']):
        """Display transactions in a tabular format."""
        table_data = [(t.date, t.description, t.amount) for t in transactions]
        print(
            tabulate(
                table_data,
                headers=['Date', 'Description', 'Amount'],
                colalign=('left', 'left', 'right'),
                tablefmt='pretty',
            )
        )
