# https://www.latlong.net/
# http://open-notify.org/Open-Notify-API/ISS-Location-Now/
# TO RUN YOUR CODE:
# https://www.pythonanywhere.com/


import requests
from datetime import datetime
import smtplib
import time

# COORDINATES OF MY CITY:
MY_LAT = 41.810478
MY_LONG = 14.378610

# MY GMAIL ACCOUNT:
my_email = "MoyTestoviyEmail@gmail.com"
password = "Privet12345"

# FUNCTION CHECKS IF ISS IS AT THE SAME POSITION AS MY CITY +- 5
def iss_overhead():
    # GETTING INFO ABOUT ISS COORDINATES:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

# CREATING A FUNCTION TO CHECK THAT IS NIGHT NOW IN MY CITY:
def is_night():
    # GETTING INFO ABOUT SUNSET AND SUNRISE IN MY CITY:
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        # to get time in unix format we use this parameter:
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    local_hour = time_now.hour


    # CHECKING IF IT DARK NOW:
    if local_hour >= sunset or local_hour <= sunrise:
        return True


# SENDING AN EMAIL ABOUT ISS:
while True:
    # we need to use a time module to slow down our cycle. we don't want it happens every second.
    time.sleep(60)
    if iss_overhead() and is_night():
        # CONNECTION:
        with smtplib.SMTP("smtp.gmail.com") as connection:

            # SECURING THE CONNECTION:
            connection.starttls()

            # LOGGING IN:
            connection.login(user=my_email, password=password)

            # SENDING EMAILS:
            connection.sendmail(
                from_addr=my_email,
                to_addrs="laramera@outlook.it",
                msg="Subject:Look up!\n\nHey!!! There is ISS above your head now! Look at the sky!"
            )
