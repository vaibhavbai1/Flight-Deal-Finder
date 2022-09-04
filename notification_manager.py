import requests
from twilio.rest import Client
import os

account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]


class NotificationManager:

    def send_message(self, money, origin_city, origin_code, destination_city, destination_code, outbound, inbound):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body=f"Low price alert! Only £{money} to fly from {origin_city}-{origin_code} to {destination_city}-{destination_code}, from {outbound} to {inbound}",
                from_=os.environ["SENDER"],
                to=os.environ["RECIVER"]
        )
        print(message.status)
