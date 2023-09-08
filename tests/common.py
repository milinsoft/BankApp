import pathlib
import unittest
from decimal import Decimal
from logging import getLogger

import settings
from app.database import Database
from app.interface.cli import BankAppCli
from app.models import Account, Base
from app.parsers import TransactionParser

# Done this way to make sure CI works
test_directory = pathlib.Path(__file__).parent.absolute().resolve() / "data"
# Paths to data folders
correct_test_files_dir = f'{test_directory}/correct'
incorrect_test_files_dir = f'{test_directory}/incorrect'

_logger = getLogger(__name__)


def convert_to_decimal(amount: float, rounding: str) -> Decimal:
    return Decimal(amount).quantize(Decimal('0.00'), rounding=rounding)


class TestBankAppCommon(unittest.TestCase):
    """Test cases for the BankAppCli class."""

    # noinspection PyPep8Naming
    # noinspection PyAttributeOutsideInit
    def setUp(self):
        """Set up the test environment."""
        self.db = Database(settings.TEST_DB_URL)
        self.session = self.db.session
        # TODO: split BankApp from BankAppCli
        self.bank_app = BankAppCli(self.session)
        self.credit_acc, self.debit_acc = self.bank_app.accounts.values()
        self.parser = TransactionParser(self.session, self.bank_app.transaction_repository)

    def tearDown(self):
        Base.metadata.drop_all(self.db.engine)

    # noinspection PyPep8Naming
    @classmethod
    def tearDownClass(cls) -> None:
        """Remove sqlite database (if applicable) after all tests run."""
        import os

        try:
            os.remove(settings.TEST_DB_URL.replace('sqlite:///', ''))
        except FileNotFoundError:
            pass
        except OSError as e:
            _logger.error(e)

    # HELPER METHODS
    def _test_account_limit(self, file_path: str, account: Account, expect_failure: bool):
        if expect_failure:
            with self.assertRaises(ValueError):
                self.parser.parse_data(file_path, account)
        else:
            data = self.parser.parse_data(file_path, account)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0].amount, -3000)
