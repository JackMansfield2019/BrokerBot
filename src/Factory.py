from DataHandler import DataHandler
from ExecutionHandler import ExecutionHandler
#from Strategy import Strategy

class DH_factory:

    # Overview: Class that creates and returns any DH object

    """
    Overview: Constructs and returns proper DH based on passed in enum

    Params: ENUM for DH_api
            params is list containg DH parameters
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid DH object based on parameter
    Throws: ValueError if parameter is invalid
    """
    def construct_dh(self, enum, params):
        if enum == 1:
            return self.dh_alpaca(params)
        elif enum == 2:
            return self.dh_binance(params)
        elif enum == 3:
            return self.dh_polygon(params)
        elif enum == 4:
            return self.dh_ibkr(params)
        elif enum == 5:
            return self.dh_alpha(params)
        else:
            raise ValueError("Invalid ENUM")
    
    """
    Overview: Constructs and returns alpaca DH based on params

    Params: params is a list of parameters for the alpaca api DH
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid alpaca DH object
    Throws: none
    """
    def dh_alpaca(self, params):
        dh = AlpacaDataHandler(params[0], params[1], params[2], params[3])
        return dh

    """
    Overview: Constructs and returns binance DH based on params

    Params: params is a list of parameters for the binance api DH
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid binance DH object
    Throws: none
    """
    def dh_binance(self, params):
        pass

    """
    Overview: Constructs and returns polygon DH based on params

    Params: params is a list of parameters for the polygon api DH
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid polygon DH object
    Throws: none
    """
    def dh_polygon(self, params):
        pass
    
    """
    Overview: Constructs and returns ibkr DH based on params

    Params: params is a list of parameters for the ibkr api DH
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid ibkr DH object
    Throws: none
    """
    def dh_ibkr(self, params):
        pass
    
    """
    Overview: Constructs and returns alpha DH based on params

    Params: params is a list of parameters for the alpha api DH 
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid alpha DH object
    Throws: none
    """
    def dh_alpha(self, params):
        pass

class EH_factory:

    # Overview: Class that creates and returns any EH object

    """
    Overview: Constructs and returns proper DH based on passed in enum

    Params: ENUM for EH_api
            params is list containg EH parameters
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid EH object based on parameter
    Throws: ValueError if parameter is invalid
    """
    def construct_eh(self, enum, params):
        if enum == 1:
            return self.eh_alpaca(params)
        elif enum == 2:
            return self.eh_binance(params)
        elif enum == 3:
            return self.eh_ibkr(params)
        elif enum == 4:
            return self.eh_alpha(params)
        else:
            raise ValueError("Invalid ENUM")
    
    """
    Overview: Constructs and returns alpaca EH based on params

    Params: params is a list of parameters for the alpaca api DH
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid alpaca DH object
    Throws: none
    """
    def eh_alpaca(self, params):
        eh = AlpacaExecutionHandler(params[0], params[1], params[2])
        return eh

    """
    Overview: Constructs and returns binance EH based on params

    Params: params is a list of parameters for the binance api EH
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid binance EH object
    Throws: none
    """
    def eh_binance(self, params):
        pass

    
    """
    Overview: Constructs and returns ibkr EH based on params

    Params: params is a list of parameters for the ibkr api EH
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid ibkr EH object
    Throws: none
    """
    def eh_ibkr(self, params):
        pass
    
    """
    Overview: Constructs and returns alpha EH based on params

    Params: params is a list of parameters for the alpha api EH 
    Requires: none
    Modifies: none
    Effects: none
    Returns: Valid alpha EH object
    Throws: none
    """
    def eh_alpha(self, params):
        pass

