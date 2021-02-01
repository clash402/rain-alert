import requests as req
from twilio.rest import Client
from decouple import config


# PROPERTIES
MY_LAT = 0
MY_LON = 0


# WEATHER
def get_weather_data():
    open_weather_map_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
    open_weather_map_key = config("OPEN_WEATHER_MAP_KEY")

    open_weather_map_params = {
        "lat": MY_LAT,
        "lon": MY_LON,
        "exclude": "current,minutely,daily",
        "appid": open_weather_map_key
    }

    res = req.get(open_weather_map_endpoint, params=open_weather_map_params)
    res.raise_for_status()
    weather_data = res.json()["hourly"][:12]

    return [hour["weather"][0] for hour in weather_data]


def will_rain(hourly_weather_data):
    for hour in hourly_weather_data:
        if hour["id"] > 900:
            return True


# MESSAGE
def will_send_message():
    if will_rain(get_weather_data()):
        twilio_account_sid = config("TWILIO_ACCOUNT_SID")
        twilio_auth_token = config("TWILIO_AUTH_TOKEN")
        twilio_client = Client(twilio_account_sid, twilio_auth_token)

        message = twilio_client.messages.create(
            body="It's going to rain today. Bring an umbrella!",
            from_=config("SENDING_PHONE_NUMBER"),
            to=config("RECEIVING_PHONE_NUMBER")
        )

        print(f"{message.status}: Message sent")
    else:
        print("No rain today")


# MAIN
will_send_message()
