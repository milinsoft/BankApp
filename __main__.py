import sys

from app import BankApp
from app.db import create_session, set_default_accounts
from settings import DB_URL


def check_python_version():
    required_python_version = (3, 11)
    current_python_version = sys.version_info[:2]
    if current_python_version < required_python_version:
        print(f"This script requires Python {required_version[0]}.{required_version[1]} or above.")
        sys.exit(1)


if __name__ == '__main__':
    check_python_version()
    db_session = create_session(DB_URL)
    app = BankApp(db_session)
    # initiate 1 credit and 1 Debit accounts.
    app.accounts = set_default_accounts(db_session)
    try:
        app.main_menu()
    except KeyboardInterrupt:
        db_session.close()
        print('\nGoodbye!')
