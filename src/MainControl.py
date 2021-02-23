import BrokerBot
import Searcher
import datetime
import pytz
import holidays
import os
import threading
from dotenv import load_dotenv


class MainControl:

    # TODO: figure out config format and proper parseing technique
    # TODO: make BB and searcher extend thread class
    def __init__(self):
        self.api_key = ""
        self.secret_key = ""
        self.base_url = ""

        try:
            self.api_key = os.environ['API_KEY']
            self.secret_key = os.environ['SECRET_KEY']
            self.base_url = os.environ['BASE_URL']
        except Exception:
            load_dotenv()
            self.api_key = os.getenv('API_KEY')
            self.secret_key = os.getenv('SECRET_KEY')
            self.base_url = os.getenv('BASE_URL')

        self.Searcher = Searcher(
            self.api_key, self.secret_key, self.base_url)
        self.BrokerBot = BrokerBot(
            self.api_key, self.secret_key, self.base_url)


def market_closed(now=None):
    tz = pytz.timezone('US/Eastern')
    us_holidays = holidays.US()

    openTime = datetime.time(hour=9, minute=30, second=0)
    closeTime = datetime.time(hour=16, minute=0, second=0)

    if not now:
        now = datetime.datetime.now(tz)

    # If a holiday
    if now.strftime('%Y-%m-%d') in us_holidays:
        return True
    # If before 0930 or after 1600
    if (now.time() < openTime) or (now.time() > closeTime):
        return True
    # If it's a weekend
    if now.date().weekday() > 4:
        return True

    return False


def run(self):
    while True:
        if market_closed:
            sleep(60)
            continue

        else:
            self.Searcher.search()
            self.BrokerBot.run()
