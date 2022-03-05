from Strategy import Strategy
from DataHandler import *
from ExecutionHandler import *
import queue
from multiprocessing import Pipe
from threading import Thread
class Trader(): 
    def __init__(self, state_size, is_eval=False, model_name=""):
        self.state_size = state_size # normalized previous days
        self.action_size = 3 # hold, buy, sell
        self.memory = deque(maxlen=1000)
        self.inventory = []
        self.model_name = model_name
        self.is_eval = is_eval
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = load_model(model_name) if is_eval else self._model()
    
    def _model(self):
        model = Sequential()
        model.add(Dense(units=64, input_dim=self.state_size, activation="relu"))
        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        return model
    
    def act(self, state):
        if not self.is_eval and random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        options = self.model.predict(state)
        return np.argmax(options[0])
    
    def expReplay(self, batch_size):
        mini_batch = []
        l = len(self.memory)
        for i in range(l - batch_size + 1, l):
            mini_batch.append(self.memory[i])
        for state, action, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    

# TODO : fix abstract class issues
class RL:
    
    def __init__(self, dh: DataHandler, eh: ExecutionHandler, ticker: str, strat_search_conn):
        self.dh = dh
        self.eh = eh
        self.ticker = ticker
        self.dh_queue = None
        self.eh_conn = None
        self.queue = []
        self.strat_search_conn = strat_search_conn
        self.target_stocks = []
       
    
    def start(self):
        
        #instantiate connections to the data handler and execution handler.
        st_dh_queue = queue.LifoQueue()
        st_eh_conn, eh_sh_conn = Pipe()
        self.set_eh_dh_conns(st_dh_queue, st_eh_conn)
        # Set queue in DH
        self.dh.set_sh_queue(st_dh_queue)

        #Thread incoming data stream from the data handler.
        dh_stream_thread = Thread(
            target=self.dh.start_streaming, args=([""],))
       
        dh_stream_thread.start()

        # dh_listen_thread = Thread(target=self.test_dh_queue, args=())
        # dh_listen_thread.start()

        searcher_thread = Thread(target=self.listen_for_searcher, args=())
        searcher_thread.start()

        
        # Initialize any technical indicators needed from the Lib.
        # Start strategy, pop stock from target stocks when needed

    
    def listen_for_searcher(self):
        while True:
            target_stock = self.strat_search_conn.recv()
            if target_stock not in self.queue:
                print(f"added {target_stock} to queue in strat")
                self.queue.append(target_stock)


    
    def next(self):
        #Buy Conditional
        #random buy thing for example.
        if self.position.size == 0:
            size = int(self.broker.getcash() / 1+ self.position.size)
            self.buy(size=size)
        # Sell Conditional
        
        pass

    
    def run_strat(self):
        #just start streaming for example.
        self.start()

        while len(self.queue) == 0:
            continue
        self.ticker = self.queue[0]
        self.pop_queue()

        for i in range(0, 5): # stays on one stock for 5 minutes, before switching to next stock in priority queue 
            self.dh.listen([self.ticker], "T")
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
    Overview: adds a stock to the queue

    Requires: none
    Modifies: self.queue
    Effects: appends "stock" to self.queue
    Returns: none
    Throws: none
    """
    def add_queue(self, stock):
        print("Adding {} to queue".format(stock))
        self.queue.append(stock)
    """
    Overview: pops a stock from the queue

    Requires: queue is not empty
    Modifies: self.queue
    Effects: appends "stock" to self.queue
    Returns: none
    Throws: RuntimeError if queue is empty
    """
    def pop_queue(self, pos=0):
        if len(self.queue) == 0:
            raise RuntimeError('cannot pop element from an empty queue') from exc
        else:
            print("Popping {} from queue".format(self.queue[pos]))
            self.queue.pop(pos)

    # need to get the stock data from data handler 
    def getStockDataVec(key):
        data = []
        #rsi = []
        #lines = open(key+".csv","r").read().splitlines()
        for line in lines[15:]:
            data.append(float(line.split(",")[1]))
            #rsi.append(float(line.split(",")[8])) 
        #return data, rsi
        return data 

    def sigmoid(x):
        return 1/(1+math.exp(-x))
    

    # cerebro gives us next data in dataframe, so need to incorporate cerebro in order to get the state 
    def getState(data, t, n): #getState(data, rsi, t, n)
        d = t - n + 1
        if d >= 0:
            block1 = data[d:t+1]
            #block2 = rsi[d:t+1] 
        else:
            block1 = -d * [data[0]] + data[0:t+1] # pad with t0
            #block2 = -d * [rsi[0]] + rsi[0:t+1] # pad with t0
        res = []
        for i in range(n-1):
            res.append((sigmoid(block1[i+1] - block1[i]))) 
            #res.append((sigmoid(block1[i+1] - block1[i])) + (sigmoid(block2[i+1] - block2[i]))) 
        return np.array([res])

    """
    def formatPrice(n):
    return("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))
    """

    def run():
        print("success")
        """
        # set as default 
        window_size = 30 

        trader = Trader(window_size)

        # set as default 
        batch_size = 32

        # need to figure out what terminated should be
        while(not terminated):
            data = self.getStockDataVec(key)
            state = getState(data, t, window_size + 1) # need to fix t
            ction = trader.act(state)

            # hold
            next_state = getState(data, t + 1, window_size + 1)
            reward = 0
    """

#---------------------------------------------------------------------------------------------------