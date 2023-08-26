from bank_app_common import *  # in this case it is safe to import all
from constants import (
    INVALID_DATA_DATE_FORMAT,
    INVALID_DATA_EMPTY_AMOUNT,
    INVALID_DATA_EMPTY_DESCRIPTION,
    INVALID_DATA_HEADER_ONLY,
    INVALID_DATA_WRONG_HEADER,
    INVALID_DATA_ZERO_AMOUNT,
    TEST_FILE_1,
    TEST_FILE_2,
    TEST_FILE_3,
    UNSUPPORTED_FILE_FORMAT,
)


class TestBankApp(BankAppCommon):
    def test_import_transactions(self):
        """Test importing transactions and checking account balance."""
        self.trx_manager_debit_acc.import_data(TEST_FILE_1)
        self.assertEqual(self.debit_acc.balance, 296_523.00)

    def test_import_file_with_invalid_date(self):
        """Test import file with incorrect date format"""
        with self.assertRaises(ValueError):
            self.trx_manager_debit_acc.import_data(INVALID_DATA_DATE_FORMAT)

    def test_import_file_without_amount(self):
        """Test import file with skipped amount"""
        with self.assertRaises(ValueError):
            self.trx_manager_debit_acc.import_data(INVALID_DATA_EMPTY_AMOUNT)

    def test_import_file_without_description(self):
        """Test import file without transaction description"""
        with self.assertRaises(ValueError):
            self.trx_manager_debit_acc.import_data(INVALID_DATA_EMPTY_DESCRIPTION)

    def test_import_transactions_header_only(self):
        """Test import correct header, but missing transactions"""
        with self.assertRaises(ValueError):
            self.trx_manager_debit_acc.import_data(INVALID_DATA_HEADER_ONLY)

    def test_import_transactions_wrong_header(self):
        """Test import data with invalid header"""
        with self.assertRaises(ValueError):
            self.trx_manager_debit_acc.import_data(INVALID_DATA_WRONG_HEADER)

    def test_import_file_with_amount_zero(self):
        """Test import file containing row with the amount 0"""
        with self.assertRaises(ValueError):
            self.trx_manager_debit_acc.import_data(INVALID_DATA_ZERO_AMOUNT)

    def test_import_transactions_from_unsupported_format(self):
        """Test import of unsupported file"""
        with self.assertRaises(ValueError):
            self.trx_manager_debit_acc.import_data(UNSUPPORTED_FILE_FORMAT)

    def test_balance_on_date(self):
        """Test account balance on specific dates."""
        self.trx_manager_debit_acc.import_data(TEST_FILE_1)

        for trx_date, trx_balance in zip(self.TEST_DATES, self.TEST_BALANCES):
            self.assertEqual(self.debit_acc.get_balance_on_date(trx_date), trx_balance)

        expected_balance = 0
        self.assertEqual(self.debit_acc.get_balance_on_date(date.min), expected_balance)

        # test balance for future date
        with self.assertRaises(AssertionError):
            self.debit_acc.get_balance_on_date(date.today() + timedelta(days=1))

    def test_debit_acc_negative_balance(self):
        """Test handling negative balance in a Debit account."""
        self._test_account_limit(TEST_FILE_2, self.debit_acc, expect_failure=True)

    def test_credit_acc_limit(self):
        """Test credit account limits."""
        self._test_account_limit(TEST_FILE_3, self.credit_acc, expect_failure=False)
        self._test_account_limit(TEST_FILE_2, self.credit_acc, expect_failure=True)

    def test_transactions_lookup_by_range(self):
        """Test transactions search by range"""
        self.trx_manager_debit_acc.import_data(TEST_FILE_1)

        # TEST_FILE_1 contains 1 transaction per date,
        # the number of found transactions should be increased by 1 by moving to the next date
        for n, _date in enumerate(self.TEST_DATES, start=1):
            self.assertEqual(n, len(self.debit_acc.get_range_transactions(end_date=_date)))

        # case where no transactions will be found
        self.assertFalse(len(self.debit_acc.get_range_transactions(end_date=date.min)))
