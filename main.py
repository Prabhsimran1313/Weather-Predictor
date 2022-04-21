from email import message
from http import client
import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


api_key = os.environ.get('OPEN_WEATHER_API')
account_sid = "ACCOUNT SID"
auth_token = "AUTH TOKEN"


your_latitude = "30.1471"
your_longitude = "78.7745"

weather_params ={
    "lat":your_latitude,
    "lon":your_longitude,
    "appid":api_key,
    "exclude":"currently, minutely, daily"
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall?", params=weather_params)
response.raise_for_status()
data = response.json()["hourly"][:11]

will_rain =False
for hours_data in data:
    condition_code = hours_data["weather"][0]["id"]
    if condition_code<700:
        will_rain =True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token,  http_client=proxy_client)
    message = client.messages \
         .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL NUMBER"
    )
     
    