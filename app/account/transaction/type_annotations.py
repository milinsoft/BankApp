from typing import Annotated

from .schemas import STransaction, STransactionAdd

TransactionsDataList = Annotated[list[STransactionAdd], "Transactions"]
TransactionsList = Annotated[list[STransaction], "Added Transactions"]
