# import DataHandler
# import ExecutionHandler
# import PortfolioManager
# import StrategyHandler
from DataHandler import AlpacaDataHandler
from threading import Thread


class BrokerBot:
    def __init__(self, api_key, secret_key, base_url, data_url):

        self.headers = {"APCA-API-KEY-ID": api_key,
                        "APCA-API-SECRET-KEY": secret_key}

        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.data_url = data_url

        self.account_url = "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)

        self.data_handler = AlpacaDataHandler(
            self.api_key, self.secret_key, self.base_url, self.data_url, "ws://127.0.0.1:8765")

        # self.stream_conn = StreamConn(
        #     api_key,
        #     secret_key,
        #     base_url=URL(self.base_url),
        #     data_url=URL(self.data_url)
        # )

    def get_account(self):
        r = requests.get(self.account_url, headers)
        return json.loads(r.content)

    def test_stream_data(self, ticker):
      self.data_handler.run_socket()
      self.data_handler.listen([ticker],"T")

      # self.data_handler.listen([ticker], "T")
