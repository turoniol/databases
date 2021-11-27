from config import DATABASE_URI
from sqlalchemy import create_engine, text, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Any

Base = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


class Repository:
    def __init__(self):
        self._session = Session()

    def get(self, entity: Any, condition: str = None, count=10, offset=0) -> Any:
        if condition is None:
            return self._session.query(entity).limit(count).offset(offset)
        return self._session.query(entity).filter(text(condition)).limit(count).offset(offset)

    def insert(self, obj: Any) -> Any:
        self._session.add(obj)
        self._commit()

    def update(self, entity: Any, condition: str, values: str) -> Any:
        d = eval(f"{{{values.replace('=', ':')}}}")
        self._session.query(entity).filter(text(condition)).update(values=d, synchronize_session='fetch')
        self._commit()

    def delete(self, entity: Any, condition: str) -> Any:
        self._session.query(entity).filter(text(condition)).delete(synchronize_session='fetch')
        self._commit()

    def _commit(self):
        self._session.commit()

    def __del__(self):
        self._session.close()
