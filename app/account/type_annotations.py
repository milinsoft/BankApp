from typing import Annotated

from sqlalchemy import Numeric
from sqlalchemy.orm import mapped_column

col_num_10_2 = Annotated[float, mapped_column(Numeric(10, 2), default=0)]
