import sqlalchemy as sq
import os
import psycopg2
import json
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


# pub1 = Publisher(name='SSS')
# pub2 = Publisher(name='AAA')
# pub3 = Publisher(name='DDD')
#
# b1 = Book(title='one', id_publisher=1)
# b2 = Book(title='two', id_publisher=2)
# b3 = Book(title='three', id_publisher=3)
# b4 = Book(title='four', id_publisher=1)
#
# s1 = Shop(name='M')
# s2 = Shop(name='5')
#
# st1 = Stock(id_book=1, id_shop=1, count=10)
# st2 = Stock(id_book=1, id_shop=2, count=20)
# st3 = Stock(id_book=2, id_shop=1, count=40)
# st4 = Stock(id_book=3, id_shop=2, count=50)
# st5 = Stock(id_book=4, id_shop=1, count=30)
# st6 = Stock(id_book=4, id_shop=1, count=30)
#
# sa1 = Sale(price=100, date_sale='01-01-2022', id_stock=1, count= 5)
# sa2 = Sale(price=120, date_sale='05-01-2022', id_stock=2, count= 3)
# sa3 = Sale(price=200, date_sale='10-01-2022', id_stock=4, count= 2)
# sa4 = Sale(price=50, date_sale='01-01-2022', id_stock=5, count= 7)
#
# session.add_all([pub1, pub2, pub3, b1, b2, b3, b4, s1, s2, st1, st2, st3, st4, st5, st6, sa1, sa2, sa3, sa4])
# session.commit()


def get_shops(id_name, session=session):
    res = session.query(
        Book.title, Shop.name, Sale.price * Sale.count, Sale.date_sale
    ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if id_name.isdigit():
        res2 = res.filter(Publisher.id == id_name).all()
    else:
        res2 = res.filter(Publisher.name == id_name).all()
    for bk, sn, sp, sd in res2:
        print(f"{bk: <40} | {sn: <10} | {sp: <8} | {sd.strftime('%d-%m-%Y')}")


with open('data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    if record['model'] == 'publisher':
        recording = Publisher(name=record['fields']['name'])
    elif record['model'] == 'book':
        recording = Book(title=record['fields']['title'], id_publisher=record['fields']['id_publisher'])
    elif record['model'] == 'shop':
        recording = Shop(name=record['fields']['name'])
    elif record['model'] == 'stock':
        recording = Stock(id_book=record['fields']['id_book'], id_shop=record['fields']['id_shop'],
                          count=record['fields']['count'])
    elif record['model'] == 'sale':
        recording = Sale(price=float(record['fields']['price']), date_sale=record['fields']['date_sale'],
                         id_stock=record['fields']['id_stock'], count=record['fields']['count'])

    session.add(recording)
    session.commit()

session.close()

if __name__ == '__main__':
    id_name = input("Введите id или имя: ")
    get_shops(id_name)
