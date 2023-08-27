import os

# done this way to make sure CI works
test_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_data'))
# paths to data folders
valid_test_files_dir = f'{test_directory}/valid'
invalid_test_files_dir = f'{test_directory}/invalid'

# test files with invalid data
UNSUPPORTED_FILE_FORMAT = f'{invalid_test_files_dir}/unsupported_file_format.jpeg'
INVALID_DATA_DATE_FORMAT = f'{invalid_test_files_dir}/incorrect_data_date_format.csv'
INVALID_DATA_EMPTY_AMOUNT = f'{invalid_test_files_dir}/incorrect_data_empty_amount.csv'
INVALID_DATA_ZERO_AMOUNT = f'{invalid_test_files_dir}/incorrect_data_zero_amount.csv'
INVALID_DATA_EMPTY_DESCRIPTION = f'{invalid_test_files_dir}/incorrect_data_empty_description.csv'
INVALID_DATA_HEADER_ONLY = f'{invalid_test_files_dir}/incorrect_data_header_only.csv'
INVALID_DATA_WRONG_HEADER = f'{invalid_test_files_dir}/incorrect_data_wrong_header.csv'

# test files with valid data
TEST_FILE_1 = f'{valid_test_files_dir}/transactions_1.csv'
TEST_FILE_2 = f'{valid_test_files_dir}/transactions_2.csv'
TEST_FILE_3 = f'{valid_test_files_dir}/transactions_3.csv'

# other constants
TEST_DATES = ('2023-04-01', '2023-04-21', '2023-05-22', '2023-06-23', '2023-07-23', '2023-08-23', '2023-08-24')
TEST_AMOUNTS = (100_000.00, 99_987.75, 99_967.5, 99_761.5, 99_761.51, 96_523.0, 296_523.0)
