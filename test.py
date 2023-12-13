import json, sys
import requests
from config import DB_CONFIG as config
from sqlalchemy.orm import declarative_base

from sqlalchemy import create_engine, Column, JSON, MetaData, String, VARCHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = f"postgresql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"


# Define the ORM model
Base = declarative_base(metadata=MetaData(schema="cards_json"))  # Specify the schema


class Card(Base):
    __tablename__ = "cards"
    id = Column(VARCHAR(50), primary_key=True)
    response_data = Column(JSON)


def create_session():
    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Create the table if it doesn't exist
    Base.metadata.create_all(bind=engine)

    # Create a session
    session = sessionmaker(bind=engine)()

    return session


def read(name):
    session = create_session()
    try:
        card = session.query(Card).filter_by(id=name).first()
        print(f"Read {name} successfully!")

        return card.response_data
    except Exception as e:
        print(f"! Failed to read card. Error: {e}")
    finally:
        session.close()


print(f'=========> {read("Forest")}')
