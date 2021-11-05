import psycopg2 as ps
from psycopg2 import sql
from psycopg2.extras import DictCursor


class Generator:
    def __init__(self):
        self.__connection = ps.connect(dbname="books", user="postgres",
                                       password="123123", host="localhost")
        self.__connection.autocommit = True

    @staticmethod
    def _generate_str(length: int) -> sql:
        queries: list = ['chr(trunc(65 + random() * 25)::int)' for i in range(length)]
        query = sql.SQL('{}').format(
            sql.SQL('||').join(map(sql.SQL, queries))
        )
        return query

    @staticmethod
    def _generate_number(inf: int, sup: int) -> sql:
        return sql.SQL('(random() * {} + {})::int').format(
            sql.SQL(str(sup - inf)),
            sql.SQL(str(inf))
        )

    @staticmethod
    def _generate_date(shift: str, inf: str, sup: str) -> sql:
        return sql.SQL('(timestamp {} + random() * (timestamp {} - timestamp {}))::date').format(
            sql.Literal(shift),
            sql.Literal(sup),
            sql.Literal(inf)
        )

    def insert_authors(self, count: int) -> None:
        query: sql = sql.SQL('insert into authors (birthday, name)'
                             'select {}, {}'
                             'from generate_series(1, {});').format(
            self._generate_date(shift='1900-01-01', sup='2100-01-01', inf='2000-01-01'),
            self._generate_str(10),
            sql.Literal(count)
        )
        with self.__connection.cursor() as cursor:
            cursor.execute(query)

    def insert_books(self, count: int) -> None:
        query: sql = sql.SQL('insert into books (year, pages, author_id, name)'
                             'select {}, {},'
                             '(select id from authors order by random() limit 1)::int,'
                             '{} from generate_series(1, {});').format(
            self._generate_number(sup=2021, inf=1930),
            self._generate_number(sup=900, inf=100),
            self._generate_str(8),
            sql.Literal(count)
        )
        with self.__connection.cursor() as cursor:
            cursor.execute(query)

    def insert_readers(self, count: int) -> None:
        query: sql = sql.SQL('insert into readers (name, money, birthday, pass_id)'
                             'select {}, {}, {},'
                             '(select id from passes order by random() limit 1) '
                             'from generate_series(1, {})').format(
            self._generate_str(5),
            self._generate_number(sup=900, inf=100),
            self._generate_date(shift='1900-01-01', sup='2100-01-01', inf='2000-01-01'),
            sql.Literal(count)
        )
        with self.__connection.cursor() as cursor:
            cursor.execute(query)

    def __del__(self):
        self.__connection.close()
