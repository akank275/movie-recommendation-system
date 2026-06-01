from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///movies.db"
)

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String,
        unique=True
    )

    password = Column(
        String
    )


class Favorite(Base):

    __tablename__ = "favorites"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String
    )

    movie = Column(
        String
    )


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()