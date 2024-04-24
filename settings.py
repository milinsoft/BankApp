from decimal import ROUND_HALF_UP

DATE_FORMAT = '%Y-%m-%d'
DB_URL = 'sqlite:///bank_app.database'
TEST_DB_URL = 'sqlite:///test_bank_app.database'
DEFAULT_CREDIT_LIMIT = -3000
ROUNDING = ROUND_HALF_UP
ORM = "sql_alchemy"
