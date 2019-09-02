from typing import Optional
from settings import db


class Model(object):
    def __init__(self, data):
        self.__dict__.update(dict(zip(data.keys(), data)))

    @classmethod
    def get(cls, pk):
        table = cls.__name__.lower() + 's'
        cursor = db.cursor()
        cursor.execute(f'select * from {table} where id = ?', [pk])
        data = cursor.fetchone()
        if data is None:
            return None
        return cls(data)

    @classmethod
    def all(cls):
        table = cls.__name__.lower() + 's'
        cursor = db.cursor()
        cursor.execute(f'select * from {table}')
        return map(cls, cursor)


class User(Model):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]


class Product(Model):
    id: int
    name: str
    price: float
    image: str
