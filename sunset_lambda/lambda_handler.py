import logging
from datetime import datetime, timedelta

import pytz
import requests

LAT = "35.787743"
LON = "-78.644257"
BASE_URL = f"https://api.sunrise-sunset.org/json?lat={LAT}&lng={LON}&formatted=0"

LOGGER = logging.getLogger(__name__)


def get_sunsetrise(date, sunriseset):
    fmt = "%Y-%m-%d"
    url = f"{BASE_URL}&date={date.strftime(fmt)}"
    LOGGER.debug(f"Hitting URL: {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.json()["results"][sunriseset]  # 2021-01-07T22:17:32+00:00


def lambda_handler(event, context):

    est = pytz.timezone("US/Eastern")
    utc = pytz.timezone("UTC")

    utc_now = utc.localize(datetime.utcnow())
    et_now = utc_now.astimezone(est)

    LOGGER.info(f"Now (UTC): {utc_now}")
    LOGGER.info(f"Now ( ET): {et_now}")

    # Get sunset
    sunset = get_sunsetrise(et_now, "sunset")

    # Get sunrise tomorrow
    sunrise = get_sunsetrise(et_now + timedelta(days=1), "sunrise")

    utc_date_format = "%Y-%m-%dT%H:%M:%S+00:00"
    utc_sunset = utc.localize(datetime.strptime(sunset, utc_date_format))
    utc_sunrise = utc.localize(datetime.strptime(sunrise, utc_date_format))
    LOGGER.info(f"Sunset (UTC): {utc_sunset}")
    LOGGER.info(f"Sunrise Tomorrow (UTC): {utc_sunrise}")

    activate = False
    if utc_sunset < utc_now < utc_sunrise:
        activate = True

    LOGGER.info(f"Activate: {activate}")

    return {"value1": "true" if activate else "false"}
