import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 0.000  # Your latitude (float)
MY_LONG = 0.000  # Your longitude (float)


def is_iss_above():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


# If the ISS is close to your current position
# and it is currently dark
# Then receive an email telling you to look up.

# Email account that sends the message
EMAIL_SENDER = "email sender"
EMAIL_SENDER_PASSWORD = "email sender password"

# Email account that receives the message
EMAIL_RECEIVER = "email receiver"

while True:
    # Check every 1 minute if the ISS is above you at night
    time.sleep(60)
    if is_iss_above() and is_night():
        # Assumes the sender is using a gmail account
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_SENDER,
            to_addrs=EMAIL_RECEIVER,
            msg="Subject:Look up\n\nThe ISS is above you in the sky."
        )
