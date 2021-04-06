from BrokerBot import BrokerBot
from Searcher import Searcher
from multiprocessing import Process, Pipe
# import Searcher
import datetime
import pytz  # pip
import holidays  # pip
import os
import threading
from dotenv import load_dotenv  # pip
import time

DEBUG = True


class MainControl:

    # TODO: figure out config format and proper parseing technique
    # TODO: make BB and searcher extend thread class
    def __init__(self):
        self.api_key = ""
        self.secret_key = ""
        self.base_url = ""
        self.socket = ""
        self.broker_bots = []
        self.searchers = []

        try:
            self.api_key = os.environ['API_KEY']
            self.secret_key = os.environ['SECRET_KEY']
            self.base_url = os.environ['BASE_URL']
            self.socket = os.environ['SOCKET']
        except Exception:
            load_dotenv()
            self.api_key = os.getenv('API_KEY')
            self.secret_key = os.getenv('SECRET_KEY')
            self.base_url = os.getenv('BASE_URL')
            self.socket = os.getenv('SOCKET')

        bb_conn, search_conn = Pipe()
        self.broker_bots.append(BrokerBot(
            self.api_key, self.secret_key, self.base_url, self.socket, bb_conn))

        self.searchers.append(Searcher(
            self.api_key, self.secret_key, self.base_url, self.socket, search_conn))

    def run(self):
        bb_proc = Process(target=self.broker_bots[0].run, args=())
        search_proc = Process(target=self.searchers[0].run, args=())
        # TODO: Implement timing algo fully
        while True:
            if market_closed and not DEBUG:
                print("MARKET CLOSED : SLEEPING FOR 1 MIN")
                time.sleep(60)
                continue

            else:
                # eventually make this loop starting bb and searchers for multiple users

                bb_proc.start()
                search_proc.start()

    # def test_data_ingest(self):
    #     # Goal : spin up several broker bots on different threads with same API key -> same socket
    #     #        see if proxy agent works with different socket instances w/ same key or need to
    #     #        instanitnate bb/searcher with one ws object
    #     broker_bots = []
    #     listening_threads = []
    #     tickers = ["TSLA", "AAPL", "GME", "AMC", "ROKU"]
    #     for i in range(2):
    #         broker_bots.append(
    #             BrokerBot(self.api_key, self.secret_key, self.base_url, self.data_url))

    #     t1 = threading.Thread(target=broker_bots[0].test_stream_data, args=(tickers[0],))
    #     t2 = threading.Thread(target=broker_bots[1].test_stream_data, args=(tickers[1],))

    #     t1.start()
    #     t2.start()
    #     # ticker_counter = 0
    #     # for bot in broker_bots:
    #     #     stream_thread = threading.Thread(
    #     #         target=bot.test_stream_data, args=(tickers[ticker_counter],))

    #     #     listening_threads.append(stream_thread)
    #     #     ticker_counter += 1

    #     # for thread in listening_threads:
    #     #     thread.start()


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


if __name__ == "__main__":
    main_control = MainControl()
    main_control.run()
