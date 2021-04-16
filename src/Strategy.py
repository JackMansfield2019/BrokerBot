from abc import ABC, abstractmethod  # Abstract class module for python.
from DataHandler import DataHandler
from ExecutionHandler import ExecutionHandler
from threading import Thread
from multiprocessing import Process, Pipe
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
    @abstractmethod
    def __init__(self, dh: DataHandler, eh: ExecutionHandler, ticker: str):
        self.dh = dh
        self.eh = eh
        self.ticker = ticker
        self.dh_queue = None
        self.eh_conn = None
    
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

        # Initialize any technical indicators needed from the Lib.

    @abstractmethod
    def next(self):
        #Buy Conditional


        # Sell Conditional    
        
        pass
   
    """
    Overview: sets the pipe connections

    Requires: none
    Modifies: none
    Effects: none
    Returns: none
    Throws: RunTimeError if any of the parameters are null
    """
    def set_eh_dh_conns(self, dh_q, eh_conn):
        if dh_q is None or eh_conn is None:
            raise RuntimeError('set_eh_dh_conns called with a null') from exc
        self.dh_queue = dh_q
        self.eh_conn = eh_conn