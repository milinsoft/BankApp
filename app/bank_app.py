from datetime import date, datetime

from sqlalchemy.exc import SQLAlchemyError
from tabulate import tabulate

from app.tools import FileManager, TransactionsManager
from settings import DATE_FORMAT


class BankApp:
    MENU_OPTIONS = {
        '0': 'Exit',
        '1': 'Import transactions (supported formats are: csv)',
        '2': 'Show balance',
        '3': 'Search transactions for the a given period',
    }
    MENU_MSG = '\n'.join((f'{k}: {v}' for k, v in MENU_OPTIONS.items()))

    def __init__(self, session):
        self.session = session
        self.accounts = {}
        self.current_account = None
        self.transactions_manager = None

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
            self.transactions_manager.import_data(FileManager.get_file_path())
            print(f'Transactions have been loaded successfully! Current balance: {self.current_account.balance}')
        except (ValueError, SQLAlchemyError) as err:
            print(err)

    def show_balance(self):
        date = self.get_date(mode='end_date')
        print(f'Your balance on {date} is: ', self.current_account.get_balance_on_date(date))

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
