import unittest
from datetime import date, timedelta
from io import StringIO
from unittest.mock import patch

import settings
from app.tests.common import TestBankAppCommon, correct_test_files_dir
from app.utils.helper_methods import to_decimal

# Test files with CORRECT data
TRANSACTIONS_1 = f"{correct_test_files_dir}/transactions_1.csv"
TRANSACTIONS_2 = f"{correct_test_files_dir}/transactions_2.csv"
TRANSACTIONS_3 = f"{correct_test_files_dir}/transactions_3.csv"

TEST_DATES = (
    date.min,
    date(2023, 4, 1),
    date(2023, 4, 21),
    date(2023, 5, 22),
    date(2023, 6, 23),
    date(2023, 7, 23),
    date(2023, 8, 23),
    date(2023, 8, 24),
)
TEST_AMOUNTS = [
    to_decimal(charge, settings.ROUNDING)
    for charge in (0, 100_000.00, 99_987.75, 99_967.5, 99_761.5, 99_761.51, 96_523.0, 296_523.0)
]


class TestBankApp(TestBankAppCommon):
    def test_01_balance_on_date(self):
        """Test account balance on specific dates."""
        # GIVEN
        parsed_data = self.parse_data(TRANSACTIONS_1, self.debit_acc_id)
        # WHEN
        self.create_transactions(self.debit_acc_id, parsed_data)
        # THEN
        for trx_date, trx_balance in zip(TEST_DATES, TEST_AMOUNTS):
            self.assertEqual(trx_balance, self.get_balance(self.debit_acc_id, trx_date))
        self.assertEqual(0, self.get_balance(self.debit_acc_id, date.min))

    def test_02_balance_on_date_future_date(self):
        """Test account balance with the future date."""
        with self.assertRaisesRegex(ValueError, "You cannot lookup in the future!"):
            self.get_balance(self.debit_acc_id, date.today() + timedelta(days=1))

    def test_03_debit_acc_negative_balance(self):
        """Test handling negative balance in a Debit and Credit accounts."""
        # GIVEN
        parsed_data = self.parse_data(TRANSACTIONS_2, self.debit_acc_id)
        # WHEN/THEN
        self._test_credit_limit(self.debit_acc_id, parsed_data, expect_error=True)
        self._test_credit_limit(self.credit_acc_id, parsed_data, expect_error=True)

    def test_04_credit_acc_limit_no_exception(self):
        # GIVEN
        parsed_data = self.parse_data(TRANSACTIONS_3, self.debit_acc_id)
        # WHEN
        transaction_ids, balance = self._test_credit_limit(self.debit_acc_id, parsed_data, expect_error=False)
        # THEN
        self.assertEqual(transaction_ids, [1])
        self.assertEqual(balance, -3000)

    def test_05_transactions_lookup_by_range(self):
        """Test transactions search by range"""
        # GIVEN
        parsed_data = self.parse_data(TRANSACTIONS_1, self.debit_acc_id)
        # WHEN
        self.create_transactions(self.debit_acc_id, parsed_data)
        # THEN
        # TRANSACTIONS_1 contains 1 transaction per date,
        # the number of found transactions should be increased by 1 by moving to the next date
        for n, _date in enumerate(TEST_DATES):
            self.assertEqual(
                n,
                len(self.bank_app.trx_service.get_by_date_range(self.bank_app.uow, self.debit_acc_id, end_date=_date)),
            )

    def test_06_get_file_path_with_retry(self):
        with patch("builtins.input", side_effect=["clearly_non_existing_path", TRANSACTIONS_1, TRANSACTIONS_2]):
            # mute prints
            with patch("sys.stdout", new=StringIO()):
                result = self.bank_app.get_file_path()
            self.assertEqual(result, TRANSACTIONS_1)


if __name__ == "__main__":
    unittest.main()
