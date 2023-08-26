from bank_app_common import *  # in this case it is safe to import all


class TestBankApp(BankAppCommon):
    def test_import_transactions(self):
        """Test importing transactions and checking account balance."""
        transactions = TransactionParser.parse_data(TEST_FILE_1)
        transactions_total = TestBankApp.get_transactions_total(transactions)
        self.assertEqual(transactions_total, 296_523.0)
        self.assertEqual(len(transactions), 7)

    def test_balance_on_date(self):
        """Test getting the account balance on specific dates."""
        transactions = TransactionParser.parse_data(TEST_FILE_1)
        self.debit_acc.balance += TestBankApp.get_transactions_total(transactions)
        self.session.add_all(self.debit_acc.create_transactions(transactions))
        self.session.commit()

        for trx_date, trx_balance in zip(self.TEST_DATES, self.TEST_BALANCES):
            self.assertEqual(self.debit_acc.get_balance_on_date(trx_date), trx_balance)

        # check balance for the date prior all transactions, expected 0
        self.assertEqual(self.debit_acc.get_balance_on_date(date.min), 0)

        # check balance for future date
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
        transactions = TransactionParser.parse_data(TEST_FILE_1)
        # create transactions objects and save to the db
        self.session.add_all(self.debit_acc.create_transactions(transactions))
        self.session.commit()

        # TEST_FILE_1 contains 1 transaction per date,
        # the number of found transactions should be increased by 1 by moving to the next date
        for n, _date in enumerate(self.TEST_DATES, start=1):
            self.assertEqual(n, len(self.debit_acc.get_range_transactions(end_date=_date)))

        # case where no transactions will be found
        self.assertFalse(len(self.debit_acc.get_range_transactions(end_date=date.min)))


if __name__ == '__main__':
    unittest.main()
