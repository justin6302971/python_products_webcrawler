from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN, DateTime,Text
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy.inspection import inspect
from os import environ

from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime

sqlalchemy_database_uri = environ.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(sqlalchemy_database_uri, echo=False, future=True)

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()
Base.metadata.schema = 'product_info'

# extension method for serialize sql objects


class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class Product(Base, Serializer):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    code = Column(String)
    description = Column(String)
    status = Column(BOOLEAN,default=True)
    created_dt = Column(DateTime,default=datetime.now())
    modified_dt = Column(DateTime)
    is_new_item = Column(BOOLEAN,default=True)
    notify_counts = Column(Integer,default=0)


    def serialize(self):
        d = Serializer.serialize(self)
        return d

    def __repr__(self):
        return f"User(id={self.id!r}, code={self.code!r}, description={self.description!r})"