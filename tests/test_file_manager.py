import unittest
from unittest.mock import patch

from constants import TEST_FILE_1, TEST_FILE_2

from app.tools.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    # noinspection PyUnusedLocal
    @patch('builtins.input', side_effect=['clearly_non_existent_path', TEST_FILE_1, TEST_FILE_2])
    def test_get_file_path_with_retry(self, mock_input):
        expected_result = TEST_FILE_1
        result = FileManager.get_file_path()
        self.assertEqual(result, expected_result)
