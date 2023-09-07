from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Account, AccountType, Base

# base must be imported from models, to proper functioning, otherwise tables won't be created.
from settings import DEFAULT_CREDIT_LIMIT


def setup_database(engine):
    Base.metadata.create_all(engine)


def create_session(db_url: str):
    engine = create_engine(db_url)
    setup_database(engine)  # Create tables if they don't exist
    return sessionmaker(bind=engine)()


def set_default_accounts(session) -> Dict[str, Account]:
    """Initialize default Debit and Credit Accounts if they don't exist."""

    debit_acc = session.query(Account).filter_by(account_type=AccountType.DEBIT.value).first()
    credit_acc = session.query(Account).filter_by(account_type=AccountType.CREDIT.value).first()

    if not debit_acc:
        debit_acc = Account(name='Debit Account', account_type=AccountType.DEBIT.value)
        session.add(debit_acc)
    if not credit_acc:
        credit_acc = Account(
            name='Credit Account', account_type=AccountType.CREDIT.value, credit_limit=DEFAULT_CREDIT_LIMIT
        )
        session.add(credit_acc)
    session.commit()
    return {'credit': credit_acc, 'debit': debit_acc}
