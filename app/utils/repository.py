from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from sqlalchemy import insert, select

from app.schemas import ModelSchema

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class AbstractRepository(ABC):
    @abstractmethod
    def create_one(self, data: "ModelSchema") -> int:
        raise NotImplementedError

    @abstractmethod
    def create_multi(self, data: list["ModelSchema"]) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    def get_one(self, filters=None, order_by=None) -> "ModelSchema":
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        filters=None,
        order_by=None,
    ) -> list["ModelSchema"]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, rec_id: int) -> "ModelSchema":
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    model: Any = None

    def __init__(self, session: "Session") -> None:
        self.session = session

    def create_one(self, data: "ModelSchema") -> int:
        data_dict = data.model_dump()
        stmt = insert(self.model).values(**data_dict).returning(self.model.id)
        res = self.session.execute(stmt).scalar_one()
        return res

    def create_multi(self, data: list["ModelSchema"]) -> list[int]:
        data_list = [d.model_dump() for d in data]
        stmt = insert(self.model).values(data_list).returning(self.model.id)
        res = self.session.execute(stmt).scalars().all()
        return res

    def _build_selectee(self, aggregate_function: Callable | None = None, column_name: str | None = None) -> Any:
        selectee = self.model
        if column_name:
            selectee = getattr(selectee, column_name)
        if aggregate_function:
            selectee = aggregate_function(selectee)
        return selectee

    # TODO: add annotations for the filters

    def get_one(self, filters=None, order_by=None) -> "ModelSchema":
        stmt = select(self.model).filter(*filters).order_by(order_by)  # type: ignore[attr-defined]
        result = self.session.execute(stmt).scalars().first()
        return result and result.to_read_model()

    def get_all(self, filters=None, order_by=None) -> list["ModelSchema"]:
        stmt = select(self.model).filter(*filters).order_by(order_by)  # type: ignore[attr-defined]
        result_rows = self.session.execute(stmt).scalars().fetchall()
        return result_rows and [result.to_read_model() for result in result_rows]

    def get_aggregated(self, aggregate_func: Callable, column_name: str, filters=None, order_by=None) -> Any:
        selectee = self._build_selectee(aggregate_func, column_name)
        stmt = select(selectee).filter(*filters).order_by(order_by)  # type: ignore[attr-defined]
        result = self.session.execute(stmt).scalars()
        return result.all()

    def get_by_id(self, rec_id: int) -> "ModelSchema":
        return self.get_one(filters=[self.model.id == rec_id])
