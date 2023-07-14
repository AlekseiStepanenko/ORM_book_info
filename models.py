import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()

publisher_book = sq.Table(
    'publisher_book', Base.metadata,
    sq.Column('publisher_id', sq.Integer, sq.ForeignKey("Publishers.id", ondelete="CASCADE")),
    sq.Column('book_id', sq.Integer, sq.ForeignKey("Books.id", ondelete="CASCADE"))
    )

class Publisher(Base):
    __tablename__ = "Publishers"

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    name = sq.Column(sq.String(length=80), unique=True, nullable=False)

    # publisher_b = relationship('Book', secondary='publisher_book', back_populates='book_publisher')

    def __str__(self):
        return f'Publishers {self.id} : {self.name}'


class Book(Base):
    __tablename__ = "Books"

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    title = sq.Column(sq.String(length=80), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, nullable=False)
    autor = sq.Column(sq.String(length=80), nullable=False)

    publisher = relationship('Publisher', backref='Books')

    # book_publisher = relationship('Publisher', secondary='publisher_book', back_populates='publisher_b')

    def __str__(self):
        return f'Books {self.id} : ({self.title}, {self.publisher})'


class Shop(Base):
    __tablename__ = "Shops"

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    name = sq.Column(sq.String(length=80), unique=True, nullable=False)

    def __str__(self):
        return f'Shops {self.id} : ({self.name}'


class Stock(Base):
    __tablename__ = "Stocks"

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('Books.id', ondelete="CASCADE"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('Shops.id', ondelete="CASCADE"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship('Book', backref='Stocks')
    shop = relationship('Shop', backref='Stocks')

    # sale_st = relationship('Sale', secondary='stock_sale', back_populates='st_sale')

    def __str__(self):
        return f'Books {self.id} : ({self.book}, {self.shop}, {self.count})'

stock_sale = sq.Table('stock_sale', Base.metadata,
    sq.Column('stock_id', sq.Integer, sq.ForeignKey("Stocks.id", ondelete="CASCADE")),
    sq.Column('sale_id', sq.Integer, sq.ForeignKey("Sales.id", ondelete="CASCADE"))
    )

class Sale(Base):
    __tablename__ = "Sales"

    id = sq.Column(sq.Integer, primary_key=True, nullable=False)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('Stocks.id', ondelete="CASCADE"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship('Stock', backref='Sales')

    # st_sale = relationship('Stock', secondary='stock_sale', back_populates='sale_st')

    def __str__(self):
        return f'Books {self.id} : ({self.price}, {self.date_sale}, {self.stock}, {self.count})'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

