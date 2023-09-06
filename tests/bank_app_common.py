"""Class setup and helper methods"""

import os
import unittest
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import BankAppCLI
from app.db import Base, setup_database
from app.models import Account, AccountType
from app.tools import TransactionsManager
from settings import DATE_FORMAT, TEST_DB_URL
from tests.constants import TEST_AMOUNTS, TEST_DATES


class BankAppCommon(unittest.TestCase):
    """Test cases for the BankAppCLI class."""

    # noinspection PyPep8Naming
    # noinspection PyAttributeOutsideInit
    def setUp(self):
        """Set up the test environment."""
        self.engine = create_engine(TEST_DB_URL)
        setup_database(self.engine)  # Create tables if they don't exist
        self.session = sessionmaker(bind=self.engine)()
        self.bank_app = BankAppCLI(self.session)
        self.debit_acc = Account(name='Test Debit Account', account_type=AccountType.DEBIT.value)
        self.credit_acc = Account(name='Test Credit Account', account_type=AccountType.CREDIT.value, credit_limit=-3000)
        self.session.add_all((self.debit_acc, self.credit_acc))
        self.session.commit()
        self.trx_manager_debit_acc = TransactionsManager(self.session, self.debit_acc)
        self.TEST_DATES = [datetime.strptime(_d, DATE_FORMAT).date() for _d in TEST_DATES]
        self.TEST_BALANCES = [self.convert_to_decimal(charge) for charge in TEST_AMOUNTS]

    # noinspection PyPep8Naming
    def tearDown(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(self.engine)

    # noinspection PyPep8Naming
    @classmethod
    def tearDownClass(cls) -> None:
        """remove db file after all tests run"""
        try:
            os.remove(TEST_DB_URL.replace('sqlite:///', ''))
        except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as e:
            print(e)

    @staticmethod
    def convert_to_decimal(amount: float) -> Decimal:
        return Decimal(amount).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    def _test_account_limit(self, test_file: str, account: Account, expect_failure: bool):
        trx_manager = TransactionsManager(self.session, account)

        if expect_failure:
            with self.assertRaises(ValueError):
                trx_manager.import_data(test_file)
        else:
            self.assertIsNone(trx_manager.import_data(test_file))
