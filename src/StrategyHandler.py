

class StrategyHandler:
    def __init__(self):
        pass

    """
    High Risk Strategy will be implemented in here.
    Below is just an example to give an idea.
    """
    def HighRisk(symbol, bars):
        fib_values = self.fibonacci(symbol, bars)
        elif current_price == fib_values[]
        for fib_val in fib_values:
            if previous_close < fib_val and current_open < fib_val:
                decision = ["SHORT", None, None] #by returning 'SHORT', this will tell execution handler to make a short trade
                return decision 
        return None
    
    def MidRisk(bars):
        pass

    """
    Low Risk Strategy will be implemented in here.
    Below is just an example to give an idea. 
    Returns:
        - Trade Decision
        - Take_Profit value
        - Stop_Loss value
    """
    def LowRisk(symbol, bars):
        vol_1 = self.volume(bars[0])
        vol_2 = self.volume(bars[1]) # I think each bar should be tuple with open, close, low, high, current prices & volume 

        if vol_1 > (vol_2 * 1.5):
            fib_values = self.fibonacci(symbol, bars)
            TP = fib_values[3] #take profit is the 3rd retracement
            SL = fib_values[2] #stop loss is the 2nd retracement
            decision =  ["BUY", TP, SL]
            return decision 
    
    def fibonacci(symbol, bars):
        first = bars[0] #first data-value in the bars array (most recent bar to current bar)
        second = bars[len(candles) - 1] #last data-value in the bars array (most farthest bar to current bar)
        retracements = [0.236, 0.382, 0.5, 0.618, 0.786]
        fib_values = [(second - ((second - first) * retracement)) for retracement in retracements]
        return fib_values 

    def Mean_Reversion:
        pass