from app.bank_app import BankApp
from app.db.db_setup import create_session, set_default_accounts
from settings import DB_URL

if __name__ == '__main__':
    db_session = create_session(DB_URL)
    app = BankApp(db_session)
    # initiate 1 credit and 1 Debit accounts.
    app.accounts = set_default_accounts(db_session)
    app.main_menu()
