from crud import Repository
from view import get_formatted_data
from models import Author, Book, Reader, Pass

r = Repository()
book = Book(year=1000, pages=300, author_id=5, name='the best book ever')
r.insert(book)
r.get(entity=Book, condition=f"id = {book.ID}")
r.update(entity=Book, condition=f"id = {book.ID}", values="pages = 400")
r.delete(entity=Book, condition=f"id = {book.ID}")
