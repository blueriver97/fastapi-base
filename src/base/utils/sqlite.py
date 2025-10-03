import logging
import traceback
from typing import List, Optional, Union

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__file__)


class SqliteManager:
    def __init__(self, address: str = "sqlite:///db.sqlite3"):
        self.address = address
        self.engine = create_engine(address, echo=False, connect_args={"check_same_thread": False})
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = self.session_maker()

    def __enter__(self) -> "SqliteManager":
        return self

    def __exit__(
        self,
        exception_type: Optional[type],
        exception_value: Optional[BaseException],
        exception_traceback: Optional[traceback.StackSummary],
    ):
        self.session.close()

    def create_table(self, orm) -> None:
        if not inspect(self.engine).has_table(orm.__tablename__):
            orm.__table__.create(bind=self.engine, checkfirst=True)
            logger.info(f"Created table({orm.__table__}).")

    def drop_table(self, orm) -> None:
        if inspect(self.engine).has_table(orm.__tablename__):
            orm.__table__.drop(bind=self.engine, checkfirst=True)
            logger.info(f"Dropped table({orm.__table__}).")

    def truncate_table(self, orm) -> None:
        if inspect(self.engine).has_table(orm.__tablename__):
            self.session.query(orm).delete()
            self.session.commit()
            logger.info(f"Truncated table({orm.__table__}).")

    def insert(self, items: Union[object, List[object]] = None, batch: int = 100) -> int:
        if items is None:
            return 0

        if not isinstance(items, list):
            items = [items]

        total = len(items)
        if total > 0:
            for i in range(0, total, batch):
                batch_items = items[i : i + batch]
                self.session.add_all(batch_items)
                self.session.commit()

        return total

    def update(self, orm, stmt, data: dict) -> None:
        try:
            self.session.query(orm).filter(stmt).update(data)
            self.session.commit()
        except Exception as e:
            logger.error(f"Update failed: {e}")
            self.session.rollback()

    def delete(self, orm, stmt) -> None:
        try:
            self.session.query(orm).filter(stmt).delete()
            self.session.commit()
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            self.session.rollback()

    def init_log(self) -> str:
        return f"Initialized database at {self.address}"
