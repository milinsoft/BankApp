from tests.common import TestBankAppCommon, correct_test_files_dir, incorrect_test_files_dir

# Test files with INCORRECT data
INCORRECT_DATA_DATE_FORMAT = f'{incorrect_test_files_dir}/date_format.csv'
INCORRECT_DATA_EMPTY_AMOUNT = f'{incorrect_test_files_dir}/empty_amount.csv'
INCORRECT_DATA_ZERO_AMOUNT = f'{incorrect_test_files_dir}/zero_amount.csv'
INCORRECT_DATA_EMPTY_DESCRIPTION = f'{incorrect_test_files_dir}/empty_description.csv'
INCORRECT_DATA_HEADER_ONLY = f'{incorrect_test_files_dir}/header_only.csv'
INCORRECT_DATA_WRONG_HEADER = f'{incorrect_test_files_dir}/header.csv'
# Test files with CORRECT data
TRANSACTIONS_1 = f'{correct_test_files_dir}/transactions_1.csv'
TRANSACTIONS_2 = f'{correct_test_files_dir}/transactions_2.csv'
TRANSACTIONS_3 = f'{correct_test_files_dir}/transactions_3.csv'


class TestFileParseCSV(TestBankAppCommon):
    def test_01_parse_transactions(self):
        """Test parseing transactions and checking account balance."""
        self.parser.parse_data(TRANSACTIONS_1, self.debit_acc)
        self.assertEqual(self.debit_acc.balance, 296_523.00)

    def test_02_parse_file_with_INCORRECT_date(self):
        """Test parse file with incorrect date format"""
        with self.assertRaises(ValueError):
            self.parser.parse_data(INCORRECT_DATA_DATE_FORMAT, self.debit_acc)

    def test_03_parse_file_without_amount(self):
        """Test parse file with skipped amount"""
        with self.assertRaises(ValueError):
            self.parser.parse_data(INCORRECT_DATA_EMPTY_AMOUNT, self.debit_acc)

    def test_04_parse_file_without_description(self):
        """Test parse file without transaction description"""
        with self.assertRaises(ValueError):
            self.parser.parse_data(INCORRECT_DATA_EMPTY_DESCRIPTION, self.debit_acc)

    def test_05_parse_transactions_header_only(self):
        """Test parse correct header, but missing transactions"""
        with self.assertRaises(ValueError):
            self.parser.parse_data(INCORRECT_DATA_HEADER_ONLY, self.debit_acc)

    def test_06_parse_transactions_wrong_header(self):
        """Test parse data with INCORRECT header"""
        with self.assertRaises(ValueError):
            self.parser.parse_data(INCORRECT_DATA_WRONG_HEADER, self.debit_acc)

    def test_07_parse_file_with_amount_zero(self):
        """Test parse file containing row with the amount 0"""
        with self.assertRaises(ValueError):
            self.parser.parse_data(INCORRECT_DATA_ZERO_AMOUNT, self.debit_acc)
