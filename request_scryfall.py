import os
import requests
import csv


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


cards = ["Forest", "Lightning Bolt"]
get_cards(cards)
