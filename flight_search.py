import requests
from datetime import datetime, timedelta
from flight_data import FlightData
import os

kiwi_endpoint = "https://tequila-api.kiwi.com/locations/query"
API_KIWI = os.environ["API_KIWI"]


class FlightSearch:

    def get_itacode(self, city_name):
        headers = {
            "apikey": API_KIWI
        }
        parameters = {
            "term": city_name,
            "location_types": "city"
        }
        kiwi_response = requests.get(url=kiwi_endpoint, params=parameters, headers=headers)
        results = kiwi_response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flight(self, origin, destination):
        today_date = datetime.now().strftime("%d/%m/%Y")
        date_of_travel = (datetime.now() + timedelta(days=6 * 30)).strftime("%d/%m/%Y")
        headers = {
            "apikey": API_KIWI
        }
        parameters = {
            "fly_from": origin,
            "fly_to": destination,
            "date_from": today_date,
            "date_to": date_of_travel,
            "curr": "GBP",
            "one_for_city": 1,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "max_stopovers": 0,
        }
        kiwi_response = requests.get(url="https://tequila-api.kiwi.com/v2/search", params=parameters, headers=headers)
        kiwi_response.raise_for_status()
        try:
            data = kiwi_response.json()["data"][0]
        except IndexError:
            print(f"No flights found to {destination}.")
            return 0

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
