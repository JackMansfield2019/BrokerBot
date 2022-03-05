from abc import ABC, abstractmethod  # Abstract class module for python.
from DataHandler import DataHandler
from ExecutionHandler import ExecutionHandler
from backtrader import backtrader as bt
from threading import Thread
from multiprocessing import Process, Pipe
from ENUMS import *
from Factory import *
import time 
import queue

"""
overview:
    - Strategy Class: Strategy is a base class for all strategies in BrokerBot.
      It takes in a DataHandler and an ExecutionHandler, which it uses to communicate
      with the given broker. (Broker type and trade type are set by the StrategyHandler)
      It then runs its strategy, which is logged continuously by Cerebro. This allows for
      backtesting and analysis of the stretegy after the fact.

Requires:   api_key,secret_key,base_url,data_url,socket, base_url, ticker,
        DH_API,EH_API,

Modifies: DH, EH,log,
Effects: DH is initialized, EH is initialized, stream is listend to, Log is initialized.
Returns: none
TODO:
    - Create more strategies.
    - Refine backtrading setup and functions.
    -
"""
class Strategy(ABC):
    """
    Class: Strategy(ABC) 
    """
    @abstractmethod
    def __init__(self, dh: DataHandler, eh: ExecutionHandler, ticker: str, strat_search_conn):
        self.dh = dh
        self.eh = eh
        self.ticker = ticker
        self.dh_queue = None
        self.eh_conn = None
        self.queue = []
        self.strat_search_conn = strat_search_conn
        self.target_stocks = []
        self.dh_factory = DH_factory()
    @abstractmethod
    def start(self):
        
        #instantiate connections to the data handler and execution handler.
        st_dh_queue = queue.LifoQueue()
        st_eh_conn, eh_sh_conn = Pipe()
        self.set_eh_dh_conns(st_dh_queue, st_eh_conn)
        # Set queue in DH
        self.DataHandler.set_sh_queue(st_dh_queue)

        #Thread incoming data stream from the data handler.
        dh_stream_thread = Thread(
            target=self.DataHandler.start_streaming, args=([""],))
        dh_listen_thread = Thread(target=self.test_dh_queue, args=())
        dh_stream_thread.start()
        dh_listen_thread.start()

        searcher_thread = Thread(target=self.listen_for_searcher, args=())
        searcher_thread.start()

        
        # Initialize any technical indicators needed from the Lib.
        # Start strategy, pop stock from target stocks when needed

    @abstractmethod
    def listen_for_searcher(self):
        while True:
            target_stock = self.strat_search_conn.recv()
            if target_stock not in self.target_stocks:
                self.target_stocks.append(target_stock)


    @abstractmethod
    def next(self):
        #Buy Conditional
        #random buy thing for example.
        if self.position.size == 0:
            size = int(self.broker.getcash() / 1+ self.position.size)
            self.buy(size=size)
        # Sell Conditional
        
        pass

    @abstractmethod
    def run_strat(self):
        #just start streaming for example.
        self.start()
        self.ticker = self.queue[0]
        self.pop_queue()

        for i in range(0, 5): # stays on one stock for 5 minutes, before switching to next stock in priority queue 
            self.dh.start_streaming(self.ticker)
            previous_time = int(time.time() - 60)
            current_time = int(time.time())
            df_price = self.df.get_bars(ticker, previous_time, current_time, "1Min", "2")

            #df_current = self.st_dh_queue.pop() 
            #df_previous = self.st_dh_queue.pop() 

            #previous_close = df_previous["close"]
            #previous_open = df_previous["open"]
            previous_close = df_price.iloc[1, 4]
            previous_open = df_price.iloc[1, 1]
            previous_candle = previous_close - previous_open 

            #current_close = df.current["close"]
            #current_open = df.current["open"]
            current_close = df_price.iloc[0, 4]
            current_open = df_price.iloc[0, 1] 
            current_candle = current_close - current_open 

            # Bullish Engulfing Buy Condition 
            if (previous_candle < 0 and current_candle > 0) and (current_open <= previous_open and current_close > previous_close):
                signal = 'buy'
                #self.eh.start_streaming(signal) 
                #money_alloc = self.eh.money_alloc_pre(0.0025, 15) 
                self.eh.create_order(self.ticker, 5, signal, 'market', 'gtc') 

            # Bearish Engulfing Sell Condition 
            if (previous_candle > 0 and current_candle < 0) and (current_open >= previous_open and current_close < previous_close):
                signal = 'sell'
                #self.eh.start_streaming(signal) 
                self.eh.create_order(self.ticker, 5, signal, 'market', 'gtc')

            #time.sleep(60)
            #next_time = current_time + 60
            #next_time = round(current_time + 60, 0) 
            next_time = current_time + 60 
            while time.time() < next_time:
                #time.sleep(1) 

                """    
                if time.time() = next_time:
                    continue 
                else:
                    time.sleep(1) 
                """ 
   
    def set_eh_dh_conns(self, dh_q, eh_conn):
        '''
        Sets the pope connections

            Parameters:
                dh_q (...): ...
                eh_conn (...): ...

            Throws: RuntimeError if any of the parameters are null 
        '''
        if dh_q is None or eh_conn is None:
            raise RuntimeError('set_eh_dh_conns called with a null') from exc
        self.dh_queue = dh_q
        self.eh_conn = eh_conn

    def add_queue(self, stock):
        '''
        Adds a stock to the queue

            Parameters:
                stock (...): a security that will be traded 
        '''
        printf("Adding {} to queue".format(stock))
        self.queue.append(stock)

    def pop_queue(self, pos=0):
        '''
        Pops a stock from the queue 

            Parameters:
                pos (int): The selected index in the queue (set to 0 as default) 
            
            Throws: 
                RuntimeError if queue is empty 
        '''
        if len(self.queue) == 0:
            raise RuntimeError('cannot pop element from an empty queue') from exc
        else:
            printf("Popping {} from queue".format(self.queue[pos]))
            self.queue.pop(pos)