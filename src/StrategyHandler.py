from DataHandler import AlpacaDataHandler
from ExecutionHandler import AlpacaExecutionHandler
from threading import Thread
import queue
import copy
from multiprocessing import Process, Pipe


"""
    Overview:
        class that handles running our different strategies, using DH & EH's that are 
        customized to what ever api constructed with
    TODO:
        construct proper DH, and EH for whatever APi selected
            select from avaliable DH's ex binance DH, alpaca DH, .. ect.
        decide what fucntion/ stratey its running
            ex. longterm, short term, medium term... ect.
        instanciate member variables    
            log(Data structure communicating with the DH)
            DH
            EH
    """


class StrategyHandler:
    # ====================Creators====================
    """
    Overview: High-Risk Strategy will be implemented here. Below is just an example to give an idea. 

    Requires:   api_key,secret_key,base_url,data_url,socket, base_url, ticker,
                DH_API,EH_API,

    Modifies: DH, EH,log,
    Effects: DH is initialized, EH is initialized, stream is listend to, Log is initialized.
    Returns: none
    """

    def __init__(self, api_key, secret_key, base_url, socket, strategy, strat_input):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.socket = socket
        self.strategy_category = strategy
        self.strategy_input = strat_input

        self.bb_conn = bb_conn
        self.dh_queue = None
        self.eh_conn = None
        self.target_stocks = []
    # ====================Observers====================
    """
    Overview: tests & prints if we revieved a message from the DH

    Requires: none
    Modifies: none
    Effects: none
    Returns: none
    Throws: none
    """

    def test_dh_queue(self):
        while True:
            data_frame = self.dh_queue.get()
            print(f"SH RECV: {data_frame}")
    # ====================Producers====================
    # ====================Mutators====================

    """
    Example Trading strategy
        def shortTerm(ticker):
            listen to stream of ticker\            
                    start adding to the message log
            while(true):
                add to the message log
                stat calculations for the strategy
                calculate trade signal 
                EH.enterTrade(ticker, signal)
                while(order has not been fullfilled){
                    // check if order fullfuill has been recieved
                    // add to log
                    //continue contiuous calculations
                }
                begin dynamic stop loss caluclations, by continuing the technical indicator calculations
                stoploss();
    """

    """
    Overview: High-Risk Strategy will be implemented here. Below is just an example to give an idea. 

    Requires: bars is non-null
    Modifies: none
    Effects: none
    Returns: sell-trade decision if previous close is less than fibonacci value AND current open is less than fibonacci value, else returns none representing no decision is made
    """
    def HighRisk(symbol, bars):
        fib_values = self.fibonacci(symbol, bars)
        # elif current_price == fib_values[]
        for fib_val in fib_values:
            if previous_close < fib_val and current_open < fib_val:
                # by returning 'SHORT', this will tell execution handler to make a short trade
                decision = ["SHORT", None, None]
                return decision
        return None

    """
    Overview: Medium-Risk Strategy will be implemented here. Below is just an example to give an idea. 

    Requires: bars is non-null
    Modifies: none
    Effects: none
    Returns: buy-trade decision, take-profit, and stop-loss if current volume is 1.5x greater than previous volume. 
    """
    def MidRisk(bars):
        pass

    """
    Overview: Low-Risk Strategy will be implemented here. Below is just an example to give an idea. 

    Requires: bars is non-null
    Modifies: none
    Effects: none
    Returns: buy-trade decision, take-profit, and stop-loss if current volume is 1.5x greater than previous volume. 
    """
    def LowRisk(symbol, bars):
        vol_1 = self.volume(bars[0])
        # I think each bar should be tuple with open, close, low, high, current prices & volume
        vol_2 = self.volume(bars[1])

        if vol_1 > (vol_2 * 1.5):
            fib_values = self.fibonacci(symbol, bars)
            TP = fib_values[3]  # take profit is the 3rd retracement
            SL = fib_values[2]  # stop loss is the 2nd retracement
            decision = ["BUY", TP, SL]
            return decision

    """
    Overview: calculates the fibonacci values of 23.6%, 38.2%, 50%, 61.8%, and 78.6% 

    Requires: bars is non-null
    Modifies: none
    Effects: none
    Returns: fibonacci values 
    Throws: RunTimeException if bars or symbol is null
    """
    def fibonacci(symbol, bars):
        if symbol is None or bars is None:
            raise RuntimeError('fibonacci called with a null') from exc
        # first data-value in the bars array (most recent bar to current bar)
        first = bars[0]
        # last data-value in the bars array (most farthest bar to current bar)
        second = bars[len(candles) - 1]
        retracements = [0.236, 0.382, 0.5, 0.618, 0.786]
        fib_values = [(second - ((second - first) * retracement))
                      for retracement in retracements]
        return fib_values
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


    """
    Overview: Create DH + EH process and pipe connection points for both

    Requires: none
    Modifies: DataHandler,
    Effects: DataHandeler starts a stream on ticket "TSLA"
    Returns: none
    Throws: none
    TODO: figure out best way to pass these pipe connections points to DH and EH
    TODO: add logic in SH and EH for using pipe to communication with SH
    """

    def run(self):
       # TODO: add logic for starting proper strategies from a given categroy
        sample_strategies = ["strat1", "strat2", "strat3"]
        searcher_strat_conns = []
        # add switch statement for instantiating correct strategy class based on strat ^
        for start in sample_strategies:
            dh_params = [self.api_key, self.secret_key, self.base_url, self.socket]
            st_dh = self.dh_factory.construct_dh(self.strategy_input[2], dh_params)
            eh_params = [self.api_key, self.secret_key, self.base_url]
            st_eh = self.eh_factory.construct_eh(self.strategy_input[3], eh_params)
            search_strat, strat_search = Pipe()

            # replace with real class
            self.strategies.append(Strategy(st_dh, st_eh, "None", strat_search))
            searcher_strat_conns.append(search_strat)

        self.searcher = Searcher(self.api_key, self.secret_key, self.base_url, self.socket, searcher_strat_conns)

        searcher_proc = Process(target=self.searcher.search, args=())
        searcher_proc.start()

        strategy_processes = []
        for strat in self.strategies:
            strat_proc = Process(target=strat.start, args=())
            strat_proc.start()
            strategy_processes.append(strat_proc)            
       

        dh_listen_thread = Thread(target=self.test_dh_queue, args=())

        dh_stream_thread.start()
        dh_listen_thread.start()



        prev_target_stocks = copy.deepcopy(self.target_stocks)
        # TODO: create logic for determining channel name based on strat
        channel_name = "T"
        # TODO: refine this once searcher routine more explictily defined
        while True:
            # if BB updates us with new target stocks from searcher, clean up DH process and start new one with updated target stocks
            new_target_stocks = self.bb_conn.recv()
            target_tickers = set(prev_target_stocks + new_target_stocks)
            self.DataHandler.listen(target_tickers, channel_name)

        
