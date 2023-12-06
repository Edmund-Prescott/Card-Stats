import os
import requests
from sqlalchemy import create_engine
from config import DB_CONFIG as db
import psycopg2


def get_cards(card_names):
    # Scryfall API endpoint for card information
    api_url = "https://api.scryfall.com/cards/named"

    results = []

    # Make batch API request for multiple cards
    for card_name in card_names:
        params = {"exact": card_name}
        response = requests.get(api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            card_data = response.json()

            print(card_data)
            # TODO: Save cards to Postgres seever
        else:
            # If the request was not successful, print an error message
            print(f"Error: {response.status_code}")

    return results


# cards = ["Forest", "Lightning Bolt"]
# get_cards(cards)

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace 'your_username', 'your_password', 'your_host', 'your_database' with your actual PostgreSQL credentials
DATABASE_URL = (
    f"postgresql://{db['user']}:{db['password']}@{db['host']}/{db['database']}"
)


try:
    # Attempt to create an engine and connect to the database
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Connected to the database successfully!")
except Exception as e:
    print(f"Failed to connect to the database. Error: {e}")
finally:
    # Close the connection if it was opened
    if "connection" in locals():
        connection.close()
