import unittest
from datetime import date, datetime, timedelta
from unittest.mock import patch

import settings
from tests.common import TestBankAppCommon, convert_to_decimal, correct_test_files_dir

# Test files with CORRECT data
TRANSACTIONS_1 = f'{correct_test_files_dir}/transactions_1.csv'
TRANSACTIONS_2 = f'{correct_test_files_dir}/transactions_2.csv'
TRANSACTIONS_3 = f'{correct_test_files_dir}/transactions_3.csv'

TEST_DATES = [
    datetime.strptime(_d, settings.DATE_FORMAT).date()
    for _d in ("2023-04-01", "2023-04-21", "2023-05-22", "2023-06-23", "2023-07-23", "2023-08-23", "2023-08-24")
]
TEST_AMOUNTS = [
    convert_to_decimal(charge, settings.ROUNDING)
    for charge in (100_000.00, 99_987.75, 99_967.5, 99_761.5, 99_761.51, 96_523.0, 296_523.0)
]


class TestBankApp(TestBankAppCommon):
    def test_01_balance_on_date(self):
        """Test account balance on specific dates."""
        self.parser.parse_data(TRANSACTIONS_1, self.debit_acc)

        for trx_date, trx_balance in zip(TEST_DATES, TEST_AMOUNTS):
            self.assertEqual(trx_balance, self.bank_app.account_repository.get_balance(self.debit_acc, trx_date))

        expected_balance = 0
        self.assertEqual(expected_balance, self.bank_app.account_repository.get_balance(self.debit_acc, date.min))

        # test balance for future date
        with self.assertRaisesRegex(ValueError, "You cannot lookup in the future!"):
            self.bank_app.account_repository.get_balance(self.debit_acc, date.today() + timedelta(days=1))

    def test_02_debit_acc_negative_balance(self):
        """Test handling negative balance in a Debit account."""
        self._test_account_limit(TRANSACTIONS_2, self.debit_acc, expect_failure=True)

    def test_03_credit_acc_limit(self):
        """Test credit account limits."""
        self._test_account_limit(TRANSACTIONS_3, self.credit_acc, expect_failure=False)
        self._test_account_limit(TRANSACTIONS_2, self.credit_acc, expect_failure=True)

    def test_04_transactions_lookup_by_range(self):
        """Test transactions search by range"""
        self.parser.parse_data(TRANSACTIONS_1, self.debit_acc)

        # TRANSACTIONS_1 contains 1 transaction per date,
        # the number of found transactions should be increased by 1 by moving to the next date
        for n, _date in enumerate(TEST_DATES, start=1):
            self.assertEqual(
                n, len(self.bank_app.transaction_repository.get_by_date_range(self.debit_acc, end_date=_date))
            )

        # case where no transactions will be found
        self.assertFalse(len(self.bank_app.transaction_repository.get_by_date_range(self.debit_acc, end_date=date.min)))

    @patch("builtins.input", side_effect=["clearly_non_existing_path", TRANSACTIONS_1, TRANSACTIONS_2])
    def test_05_get_file_path_with_retry(self, mock_input):
        expected_result = TRANSACTIONS_1
        result = self.bank_app.get_file_path()
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
