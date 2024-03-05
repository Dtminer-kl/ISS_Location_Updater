import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 3.138270
MY_LONG = 101.608047


def close_by():
    """Returns True if ISS is within 5 degrees of Location"""
    # Get Location of Internation Space Station from API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Position is within +5 or -5 degrees of the ISS position
    if (iss_latitude - MY_LAT) <= 5 and (iss_longitude - MY_LONG) <= 5:
        return True
    else:
        return False


def is_dark():
    """Return True when it is dark"""

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # Check to see if dark AKA sunset
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now < sunset or time_now > sunrise:
        return False
    else:
        return True


# Setting email, app password
sending_email = "dixontankl@outlook.com"
receiving_email = "dixontankl@yahoo.com"
app_password = "yciewxqoeftednxo"

while True:
    time.sleep(60)
# Send Email if ISS is nearby and at night (better visibility)
    if close_by() and is_dark():
        with smtplib.SMTP("smtp-mail.outlook.com", port=587) as connection:
            connection.starttls()
            connection.login(user=sending_email, password=app_password)
            connection.sendmail(
                from_addr=sending_email,
                to_addrs=receiving_email,
                msg="Subject: LOOK UP\n\n"
                    "The ISS is around your location"
            )
