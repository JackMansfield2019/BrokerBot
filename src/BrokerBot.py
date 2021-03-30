# import DataHandler
# import ExecutionHandler
# import PortfolioManager
# import StrategyHandler
from StrategyHandler import StrategyHandler
from threading import Thread
import time
from multiprocessing import Process
import os


class BrokerBot:
    def __init__(self, api_key, secret_key, base_url, socket):

        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key
        }

        self.market_open = True
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.socket = socket

        self.account_url = "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)

        self.strategy_handler_processes = []

        # self.stream_conn = StreamConn(
        #     api_key,
        #     secret_key,
        #     base_url=URL(self.base_url),
        #     data_url=URL(self.data_url)
        # )

    def set_market_close(self):
        self.market_open = False

    def get_account(self):
        r = requests.get(self.account_url, headers)
        return json.loads(r.content)

    # Start SH on own process via multiprocessing
    # TODO: figure out strategy logic/pipeline
    def run(self):
        # strategies = ["ST1", "ST2", "ST3"]
        strategies = ["ST1"]
        sh_instances = []
        sh_processes = []
        for strat in strategies:
            sh_instances.append(StrategyHandler(
                self.api_key, self.secret_key, self.base_url, self.socket, strat))

        for sh in sh_instances:
            sh_processes.append(Process(target=sh.run, args=()))

        for proc in sh_processes:
            proc.start()

        while True:
            if not self.market_open:
                for proc in sh_processes:
                    proc.join()
            else:
                time.sleep(60)
