from app.tests.common import TestBankAppCommon, incorrect_test_files_dir

UNSUPPORTED_FILE_FORMAT = f'{incorrect_test_files_dir}/unsupported_file_format.jpeg'


class TestTransactionParser(TestBankAppCommon):
    def test_01_parsing_strategy_unsupported_format(self):
        """Test import of unsupported file"""
        with self.assertRaises(ValueError):
            self.bank_app.parser.parse_data(UNSUPPORTED_FILE_FORMAT)
