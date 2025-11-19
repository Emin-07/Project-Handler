from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    declared_attr,
)
from sqlalchemy import create_engine
from .db_config import settings
from typing import List


sync_engine = create_engine(url=settings.DATABASE_url_psycopg, echo=False)
async_engine = create_async_engine(url=settings.DATABASE_url_asyncpg, echo=False)

sync_session_factory = sessionmaker(
    bind=sync_engine, autoflush=False, autocommit=False, expire_on_commit=False
)
async_session_factory = async_sessionmaker(
    bind=async_engine, autoflush=False, autocommit=False, expire_on_commit=False
)


class Base(DeclarativeBase):
    __abstract__ = True
    cols_amount: int = 100

    # @declared_attr.directive
    # def __tablename__(self) -> str:
    #     pass

    def __repr__(self) -> str:
        table_column_names = self.__table__.columns.keys()
        res: List[str] = []
        for idx, col in enumerate(table_column_names):
            if idx < self.cols_amount:
                res.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__}: {', '.join(res)}>"


class Base2(DeclarativeBase):
    __abstract__ = True
    cols_amount: int = 100

    def __repr__(self) -> str:
        table_column_names = self.__table__.columns.keys()
        res: List[str] = []
        for idx, col in enumerate(table_column_names):
            if idx < self.cols_amount:
                res.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__}: {', '.join(res)}>"
