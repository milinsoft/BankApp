from datetime import date, datetime
from logging import getLogger
from os.path import exists

from sqlalchemy.exc import SQLAlchemyError
from tabulate import tabulate

import settings
from app.models import BankApp, Transaction

_logger = getLogger(__name__)


class BankAppCli(BankApp):
    MENU_OPTIONS = {
        '0': 'Exit',
        '1': 'Import transactions (supported formats are: csv)',
        '2': 'Show balance',
        '3': 'Search transactions for the a given period',
    }
    MENU_MSG = '\n'.join((f'{k}: {v}' for k, v in MENU_OPTIONS.items()))

    def main_menu(self):
        print('Welcome to the Bank App!')
        self.current_account = self.pick_account()
        actions = {'0': self.exit_app, '1': self.import_data, '2': self.show_balance, '3': self.search_transactions}
        while True:
            action = self.get_valid_action()
            actions[action]()

    def import_data(self):
        try:
            self.parser.parse_data(self.get_file_path(), self.current_account)
            print(f'Transactions have been loaded successfully! Current balance: {self.current_account.balance}')
        except (ValueError, SQLAlchemyError) as err:
            _logger.error(err)

    @classmethod
    def get_file_path(cls) -> str:
        while True:
            file_path = input('Please provide the path to your file: ').strip("'\"")
            if not exists(file_path):
                print('Incorrect file path, please try again!')
            else:
                return file_path

    def show_balance(self):
        target_date = self.get_date(mode='end_date')
        print(
            f'Your balance on {target_date} is: ',
            self.account_repository.get_balance(self.current_account, target_date),
        )

    def search_transactions(self):
        transactions = self.transaction_repository.get_by_date_range(
            self.current_account, self.get_date('start_date'), self.get_date('end_date')
        )
        if not transactions:
            print('No transactions found!')
        else:
            self.display_transactions(transactions)

    @classmethod
    def get_valid_action(cls):
        print('\nWelcome to the main menu, how can I help you today?: ')
        action = False
        while action not in cls.MENU_OPTIONS.keys():
            action = input(f'{cls.MENU_MSG}\n').strip()
        return action

    @staticmethod
    def get_date(mode):
        assert mode in (allowed_modes := ('start_date', 'end_date')), 'invalid mode'
        today_date = date.today()

        msg = (
            f'\nProvide the {mode} in the following {datetime.strftime(today_date, settings.DATE_FORMAT)} format or\n'
            'press enter/return to '
        )
        msg += 'search from the oldest transaction\n' if mode == allowed_modes[0] else "pick today's date by default!\n"

        while True:
            target_date = input(msg).strip()
            if not target_date:
                return datetime.min.date() if mode == allowed_modes[0] else today_date
            try:
                target_date = datetime.strptime(target_date, settings.DATE_FORMAT).date()
                assert target_date <= today_date, 'Cannot lookup in the future! :)'
            except ValueError:
                _logger.error('Incorrect data format')
            except AssertionError as err:
                _logger.error(err)
            else:
                return target_date

    def pick_account(self):
        acc = False
        while acc not in ('d', 'c'):
            acc = input('Pick an account: Debit or Credit (d/c): ').lower().strip()
        return self.accounts['debit'] if acc == 'd' else self.accounts['credit']

    @classmethod
    def display_transactions(cls, transactions: list[Transaction]) -> None:
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

    def exit_app(self):
        self.session.close()
        exit(print('Goodbye!'))
