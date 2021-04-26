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
    
    
class RL(Strategy):
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
        # set as default 
        window_size = 30 

        trader = Trader(window_size)

        # set as default 
        batch_size = 32

        # need to figure out what terminated should be
        while(not terminated):
            data = self.getStockDataVec(key):
            state = getState(data, t, window_size + 1) # need to fix t
            ction = trader.act(state)

            # hold
            next_state = getState(data, t + 1, window_size + 1)
            reward = 0

#---------------------------------------------------------------------------------------------------