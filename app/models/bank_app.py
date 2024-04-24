from importlib import import_module
from typing import TYPE_CHECKING, Optional

import settings
from app.models.orm_independent import AccountType
from app.parsers import TransactionParser

CREDIT = AccountType.CREDIT.value
DEBIT = AccountType.DEBIT.value

orm = import_module(f"app.repositories.{settings.ORM}")

if TYPE_CHECKING:
    from app.models import Account, Transaction


class BankApp:
    def __init__(self, session) -> None:
        self.session = session
        self.account_repository = orm.AccountRepository(self.session)
        self.transaction_repository = orm.TransactionRepository(self.session)
        self.accounts: dict[str, "Account"] = self.set_default_accounts()
        self.current_account: Optional["Account"] = None
        self.parser = TransactionParser(self.session, self.transaction_repository)

    def main_menu(self):
        raise NotImplementedError

    def show_balance(self):
        raise NotImplementedError

    def search_transactions(self):
        raise NotImplementedError

    def pick_account(self):
        raise NotImplementedError

    @classmethod
    def display_transactions(cls, transactions: list["Transaction"]):
        raise NotImplementedError

    def set_default_accounts(self) -> dict[str, "Account"]:
        """Initialize default Debit and Credit Accounts if they don't exist."""
        debit_acc = self.account_repository.get_by_type(DEBIT) or self.account_repository.create(
            name="Debit Account", account_type=DEBIT
        )
        credit_acc = self.account_repository.get_by_type(CREDIT) or self.account_repository.create(
            name="Credit Account",
            account_type=CREDIT,
            credit_limit=settings.DEFAULT_CREDIT_LIMIT,
        )
        self.session.add_all([debit_acc, credit_acc])
        self.session.commit()
        return {"credit": credit_acc, "debit": debit_acc}
