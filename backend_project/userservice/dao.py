from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URI = 'sqlite:///user.db'

Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(DB_URI))
session = scoped_session(Session)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_json(self):
        to_serailize = ['id', 'name', 'email']
        d = {}
        for attr in to_serailize:
            d[attr] = getattr(self, attr)
        return d

if __name__ == "__main__":
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
