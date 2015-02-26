from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'),
                             nullable=False)
    bids = relationship("Bid",backref="item")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    items = relationship("Item", backref="user")
    bids = relationship("Bid", backref="user")

class Bid(Base):
    __tablename__ = "bid"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'),
                             nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'),
                             nullable=False)

Base.metadata.create_all(engine)

beyonce = User()
beyonce.user_name = "bknowles"
beyonce.password = "crazyinlove"
session.add(beyonce)
session.commit()

nara = User()
nara.user_name = "nmanjate"
nara.password = "moyra"
session.add(nara)
session.commit()

john = User()
john.user_name = "jgoodacre"
john.password = "hello"
session.add(john)
session.commit()

baseball = Item(name="Baseball", description="Round thing", user=beyonce)
session.commit()

basebidj = Bid(price=10.0, user=john, item=baseball)
basebidn = Bid(price=11.0, user=nara, item=baseball)

max_price = 0.0
highest_bidder=""
for bid_item in baseball.bids:
    if bid_item.price>max_price:
        max_price = bid_item.price
        highest_bidder=bid_item.user.user_name
print highest_bidder
