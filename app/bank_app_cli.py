from datetime import date, datetime
from os.path import exists
from typing import Dict, Optional

from app.models import Account
from app.tools import TransactionsManager
from settings import DATE_FORMAT
from sqlalchemy.exc import SQLAlchemyError


class BankAppCLI:
    MENU_OPTIONS = {
        '0': 'Exit',
        '1': 'Import transactions (supported formats are: csv)',
        '2': 'Show balance',
        '3': 'Search transactions for the a given period',
    }
    MENU_MSG = '\n'.join((f'{k}: {v}' for k, v in MENU_OPTIONS.items()))

    def __init__(self, session):
        self.session = session
        self.accounts: Dict[str, Account] = {}
        self.current_account: Optional[Account] = None
        self.transactions_manager: Optional[TransactionsManager] = None

    def main_menu(self):
        print('Welcome to the Bank App!')
        self.current_account = self.pick_account()
        self.transactions_manager = TransactionsManager(self.session, self.current_account)
        actions = {'0': self.exit_app, '1': self.import_data, '2': self.show_balance, '3': self.search_transactions}

        while True:
            action = self.get_valid_action()
            actions[action]()

    def import_data(self):
        try:
            self.transactions_manager.import_data(self.get_file_path())
            print(f'Transactions have been loaded successfully! Current balance: {self.current_account.balance}')
        except (ValueError, SQLAlchemyError) as err:
            print(err)

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
        print(f'Your balance on {target_date} is: ', self.current_account.get_balance_on_date(target_date))

    def search_transactions(self):
        transactions = self.transactions_manager.search_transactions(
            self.get_date('start_date'), self.get_date('end_date')
        )
        if not transactions:
            print('No transactions found!')
        else:
            self.transactions_manager.display_transactions(transactions)

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
            f'\nProvide the {mode} in the following {datetime.strftime(today_date, DATE_FORMAT)} format or\n'
            'press enter/return to '
        )
        msg += 'search from the oldest transaction\n' if mode == allowed_modes[0] else "pick today's date by default!\n"

        target_date = False

        while not target_date:
            target_date = input(msg).strip()
            if not target_date:
                return datetime.min.date() if mode == allowed_modes[0] else today_date
            try:
                target_date = datetime.strptime(target_date, DATE_FORMAT).date()
                assert target_date <= today_date, 'Cannot lookup in the future! :)'
            except ValueError:
                print('Incorrect data format')
                target_date = False
            except AssertionError as err:
                print(err)
                target_date = False
        return target_date

    def pick_account(self):
        acc = False
        while acc not in ('d', 'c'):
            acc = input('Pick an account: Debit or Credit (d/c): ')
        return self.accounts['debit'] if acc == 'd' else self.accounts['credit']

    def exit_app(self):
        self.session.close()
        exit(print('Goodbye!'))
