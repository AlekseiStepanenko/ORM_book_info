import sqlalchemy as sq
import os
import psycopg2
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from pprint import pprint

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
BD = os.getenv('BD')

DSN = f'postgresql://{LOGIN}:{PASSWORD}@localhost:5432/{BD}'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

pub1 = Publisher(name='SSS')
pub2 = Publisher(name='AAA')
pub3 = Publisher(name='DDD')

b1 = Book(title='one', id_publisher=1, autor='Пушкин')
b2 = Book(title='two', id_publisher=2, autor='Толстой')
b3 = Book(title='three', id_publisher=3, autor='Достоевский')
b4 = Book(title='four', id_publisher=1, autor='Твен')

s1 = Shop(name='M')
s2 = Shop(name='5')

st1 = Stock(id_book=1, id_shop=1, count=10)
st2 = Stock(id_book=1, id_shop=2, count=20)
st3 = Stock(id_book=2, id_shop=1, count=40)
st4 = Stock(id_book=3, id_shop=2, count=50)
st5 = Stock(id_book=4, id_shop=1, count=30)
st6 = Stock(id_book=4, id_shop=1, count=30)

sa1 = Sale(price=100, date_sale='01-01-2022', id_stock=1, count= 5)
sa2 = Sale(price=120, date_sale='05-01-2022', id_stock=2, count= 3)
sa3 = Sale(price=200, date_sale='10-01-2022', id_stock=4, count= 2)
sa4 = Sale(price=50, date_sale='01-01-2022', id_stock=5, count= 7)

session.add_all([pub1, pub2, pub3, b1, b2, b3, b4, s1, s2, st1, st2, st3, st4, st5, st6, sa1, sa2, sa3, sa4])
session.commit()

subq = session.query(Book.title, Book.autor, Sale.price * Sale.count, Sale.date_sale).filter(Book.autor.like(input('Введите фамилию автора: '))).subquery()

for c in session.query(Publisher).join(Book.id_publisher).join(Stock.id_book).join(Shop.id).join(Sale.id_stock).join(subq, Sale.id == subq.c.autor).all():
    print(c)


session.close()
