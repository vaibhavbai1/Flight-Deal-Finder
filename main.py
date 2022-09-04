from pprint import pprint
import requests
from flight_search import FlightSearch
from notification_manager import NotificationManager
import os


bearer_headers = {
        "Authorization": os.environ["SHEETY_VERIFICATION"]
    }

sheet_endpoint = os.environ["SHEET_ENDPOINT"]

sheety_response = requests.get(sheet_endpoint, headers=bearer_headers)
sheet_data = sheety_response.json()["prices"]

# for i in sheet_data:
#     new_data = {
#         "price": {
#             "iataCode": i["iataCode"]
#         }
#     }
#     put_response = requests.put(f"{sheet_endpoint}/{i['id']}",
#                                 json=new_data,
#                                headers=bearer_headers)
#     put_response.raise_for_status()

origin_city = "LON"
flight_search = FlightSearch()
notification = NotificationManager()
for i in sheet_data:
    flight = flight_search.check_flight(origin_city, i["iataCode"])
    if flight !=0:
        if flight.price <= i["lowestPrice"]:
            notification.send_message(flight.price, flight.origin_city, flight.origin_airport, flight.destination_city,
                                      flight.destination_airport, flight.out_date, flight.return_date)

