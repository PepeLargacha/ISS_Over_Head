import requests
from datetime import datetime
import smtplib
from time import sleep

MY_LAT = -20.336840
MY_LONG = -40.291931
MY_EMAIL = 'email@email.com'
MY_PASSWORD = 'easypassword123'
SMTP_ADRESS = "smtp.gmail.com"


def iss_over_head():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if ((MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5))and\
            ((MY_LONG - 5) <= iss_longitude <= (MY_LONG + 5)):
        return True
    else:
        return False


def get_time():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    hour = datetime.now().hour
    return sunset <= hour or hour < sunrise


while True:
    if iss_over_head() and get_time():
        with smtplib.SMTP(SMTP_ADRESS) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                                msg=f"To: {MY_EMAIL}\nSubject: Look UP!!\n\n"
                                    f"The ISS is passing over your head.")
    sleep(60)




