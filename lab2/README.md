### Назва лабораторної роботи
Створення додатку бази даних, орієнтованого на взаємодію з СУБД
PostgreSQL
### Структура бази даних
База складається з 5 таблиць (books, authors, passes, readers, 
readers_books).

Всього існує 4 сутності, і вони знаходяться у таких відношеннях:
1) pass – reader : one-to-many
2) reader – book : many-to-many
3) author – book : one-to-many

### Сторонні бібліотеки 
[psycopg2](https://www.psycopg.org/docs/)  
[pandas](https://pandas.pydata.org/)