from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Date, String, ForeignKey, Table

Base = declarative_base()

readers_books = Table('readers_books', Base.metadata,
                      Column('reader_id', ForeignKey('readers.id'), primary_key=True),
                      Column('pass_id', ForeignKey('passes.id'), primary_key=True))


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)
    books = relationship('Book', cascade='all, delete')

    def __repr__(self):
        return '<Author(id={}, name={}, birthday={})>'.\
            format(self.id, self.name, self.birthday)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    pages = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.id'))
    name = Column(String)

    def __repr__(self):
        return '<Book(id={}, year={}, pages={}, author_id{}, name={})>'.\
            format(self.id, self.year, self.pages, self.author_id, self.name)


class Pass(Base):
    __tablename__ = 'passes'
    id = Column(Integer, primary_key=True)
    cost = Column(Integer)
    duration = Column(Integer)
    name = Column(String)
    readers = relationship('Reader', cascade='all, delete')

    def __repr__(self):
        return '<Pass(id={}, cost={}, duration={}, name={})>'.\
            format(self.id, self.cost, self.duration, self.name)


class Reader(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True)
    money = Column(Integer)
    birthday = Column(Date)
    pass_id = Column(Integer, ForeignKey('passes.id'))

    def __repr__(self):
        return '<Reader(id={}, money={}, birthday={}, pass_id={})>'.\
            format(self.id, self.money, self.birthday, self.pass_id)