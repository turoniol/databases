import psycopg2 as ps
from psycopg2.extras import RealDictCursor
from psycopg2 import sql


class Repository:
    def __init__(self):
        self.__connection = ps.connect(dbname="books", user="postgres",
                                       password="123123", host="localhost")
        self.__connection.autocommit = True

    def insert(self, table: str, columns: tuple, value: tuple) -> None:
        with self.__connection.cursor() as cursor:
            query = sql.SQL('INSERT INTO {} ({}) VALUES {}').format(
                sql.Identifier(table),
                sql.SQL(',').join(map(sql.Identifier, columns)),
                sql.Literal(value)
            )
            cursor.execute(query)

    def get(self, table: str, condition: str = None, count: int = 10, offset: int = 0) -> dict:
        result: dict
        with self.__connection.cursor(cursor_factory=RealDictCursor) as cursor:
            query: sql = sql.SQL('SELECT * FROM {} ').format(
                sql.SQL(', ').join(map(sql.Identifier, table.split(', ')))
            )

            if condition is not None:
                query += sql.SQL(' WHERE {}').format(sql.SQL(condition))
            query += sql.SQL(' LIMIT {} OFFSET {}').format(
                sql.Literal(count),
                sql.Literal(offset)
            )
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def delete(self, table: str, condition: str) -> None:
        with self.__connection.cursor() as cursor:
            query = sql.SQL('DELETE FROM {} WHERE {}').format(
                sql.Identifier(table),
                sql.Literal(condition)
            )
            cursor.execute(query)

    def update(self, table: str, updated: str, condition: str) -> None:
        with self.__connection.cursor() as cursor:
            query = sql.SQL('UPDATE {} SET {} WHERE {}').format(
                sql.Identifier(table),
                sql.SQL(updated),
                sql.SQL(condition)
            )
            cursor.execute(query)

    def __del__(self):
        self.__connection.close()
