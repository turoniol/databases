import repository as r
import dataview as d
import time


class Controller:
    def __init__(self):
        self._page: int = 0
        self._rep = r.Repository()
        self._view = d.get_formatted_data

    def start(self) -> None:
        methods: dict = {
            'insert': self._on_insert,
            'update': self._on_update,
            'get': self._on_get,
            'delete': self._on_delete
        }
        while True:
            command: str = input('Введіть команду: ').strip()
            if command == 'exit':
                return
            elif command == 'help':
                self._on_help()
                continue
            try:
                method = methods[command]
                table_name: str = input('Введіть назву таблиці: ').strip()
                method(table_name)
                print('Успішно!')
            except KeyError:
                print('Такої операції не існує!')
            except Exception as err:
                print(err)

    def _on_insert(self, table_name: str) -> None:
        columns: tuple = tuple(input('Введіть назви стовпців: ').strip().split())
        values: tuple = tuple(input('Введіть значення атрибутів: ').strip().split())
        try:
            self._rep.insert(table=table_name, columns=columns, value=values)
        except Exception as err:
            print(err)

    def _on_update(self, table_name: str) -> None:
        condition = self._read_condition()
        updated = None
        while True:
            updated = input('Введіть оновлені значення: ').strip()
            if updated:
                break
        self._rep.update(table=table_name, updated=updated, condition=condition)

    def _on_delete(self, table_name: str) -> None:
        condition = self._read_condition()
        self._rep.delete(table=table_name, condition=condition)

    def _on_get(self, table_name: str) -> None:
        condition = self._read_condition()
        start = time.time()
        data: dict = self._rep.get(table=table_name, condition=condition)
        end = time.time()
        print(self._view(data))
        print(f'Час виконання запиту: {end - start} секунд.')

    @classmethod
    def _read_condition(cls) -> str:
        while True:
            condition = input('Введіть умову відбору (all для всіх): ').strip()
            if not condition:
                continue
            if condition == 'all':
                condition = None
            else:
                condition = cls._prepare_condition(condition)
            return condition

    @staticmethod
    def _prepare_condition(condition: str) -> str:
        return condition.replace(',', ' and ')

    @staticmethod
    def _on_help():
        print('date format: "year-month-year"\n'
              'table name : table1, table2, ...'
              'insert : 1) column1 column2 ... 2) value1 value2 ...\n'
              'get : 1) column1 = value1,column2 < value2,column3 like value3,... \n'
              'delete : 1) column1 = value1,...\n'
              'update : 1) column1 = value1,... 2) column1 = value1, ...\n')
