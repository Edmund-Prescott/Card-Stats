import json
import requests
from config import DB_CONFIG as config
from sqlalchemy.orm import declarative_base

from sqlalchemy import create_engine, Column, JSON, MetaData, VARCHAR
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


def fetch_cards(card_names):
    # Scryfall API endpoint for card information
    api_url = "https://api.scryfall.com/cards/named"

    results = []

    # Make batch API request for multiple cards
    for card_name in card_names:
        card_data = read_card(card_name)
        if card_data is not None:
            results.append(card_data)
            print(f"Fetched {card_name} from database successfully!")

        else:
            params = {"exact": card_name}
            response = requests.get(api_url, params=params)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                card_data = response.json()

                save_card(card_data)
                print(f"Fetched {card_name} from Scryfall successfully!")
                results.append(card_data)

            else:
                # If the request was not successful, print an error message
                print(f"Error: {response.status_code}")

    return results


def save_card(json_data):
    session = create_session()

    try:
        # Insert a row into the "cards" table with JSON data
        new_card = Card(id=json_data["name"], response_data=json.dumps(json_data))
        session.add(new_card)
        session.commit()
        print(f'{json_data["name"]} saved successfully!')
    except Exception as e:
        print(f"Failed to save card. Error: {e}")
    finally:
        # Close the session
        session.close()


def read_card(name):
    session = create_session()

    try:
        card = session.query(Card).filter_by(id=name).first()
        print(f"Read {name} successfully!")
        session.commit()
        return card.response_data
    except Exception as e:
        print(f"! Failed to read card. Error: {e}")
    finally:
        # Close the session
        session.close()


fetch_cards(["Forest", "Mountain"])
