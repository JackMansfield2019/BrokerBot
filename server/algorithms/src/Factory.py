from DataHandler import *
from ExecutionHandler import *
from Strategy import Strategy
from RL import *
#==================================================================================================================

class DH_factory:

    # Overview: Class that creates and returns any DH object
    """
    Class: DH_factory
    .............................................................................................................

    Overview
    --------
    Class that creates and returns any Data Handler (DH) object. 

    .............................................................................................................
    
    Attributes
    ----------
    N/A

    .............................................................................................................

    Methods
    -------
    construct_dh(enum, params):
        Constructs and returns proper Data Handler (DH) based on passed in enum.
    
    dh_alpaca(params):
        Constructs and returns alpaca Data Handler (DH) based on params.
    
    dh_binance(params):
        Constructs and returns binance Data Handler (DH) based on params.
    
    dh_polygon(params):
        Constructs and returns polygon Data Handler (DH) based on params.
    
    dh_ibkr(params):
        Constructs and returns ibkr Data Handler (DH) based on params.
    
    dh_alpha(params):
        Constructs and returns alpha Data Handler (DH) based on params.

    .............................................................................................................
    """

    def __init__(self):
        return
    #--------------------------------------------------------------------------------------------------------------

    def construct_dh(self, enum, params):
        '''
        Constructs and returns proper Data Handler (DH) based on passed in enum.

            Parameters:
                enum (ENUM): enumeration for DH_api (Data Handler API)
                params (list): contains Data Handler (DH) parameters 
            
            Returns: 
                Valid Data Handler Object (DH object) based on parameter 
            
            Throws:
                ValueError if parameter is invalid 
        '''
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
    #--------------------------------------------------------------------------------------------------------------
    
    def dh_alpaca(self, params):
        '''
        Constructs and returns alpaca Data Handler (DH) based on params.

            Parameters:
                params (list): parameters for the alpaca api Data Handler 
            
            Returns:
                dh: valid alpaca Data Handler object (DH object) 
        '''
        dh = AlpacaDataHandler(params[0], params[1], params[2], params[3])
        return dh
    #--------------------------------------------------------------------------------------------------------------

    def dh_binance(self, params):
        '''
        Constructs and returns binance Data Handler (DH) based on params.

            Parameters:
                params (list): parameters for the ninance api Data Handler
            
             Returns: 
                Valid binance Data Handler object (DH object)
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------

    def dh_polygon(self, params):
        '''
        Constructs and returns polygon Data Handler (DH) based on params.

            Parameters:
                params (list): parameters for the polygon api Data Handler (DH)
            
            Returns: 
                Valid polygon Data Handler (DH) object
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------
    
    def dh_ibkr(self, params):
        '''
        Constructs and returns ibkr Data Handler (DH) based on params. 

            Parameters:
                params (list): parameters for the ibkr api Data Handler 
            
            Returns: 
                Valid ibkr Data Handler object
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------

    def dh_alpha(self, params):
        '''
        Constructs and returns alpha Data Handler (DH) based on params.

            Parameters:
                params (list): parameters for the alpha api Data Handler

            Returns:   
                  Valid alpha Data Handler object
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------
#==================================================================================================================

class EH_factory:

    """
    Class: EH_factory
    .............................................................................................................

    Overview
    --------
    Class that creates and returns any Execution Handler (EH) object. 

    .............................................................................................................
    
    Attributes
    ----------
    N/A

    .............................................................................................................

    Methods
    -------
    construct_eh(enum, params):
        Constructs and returns proper EH based on passed in enum.
    
    eh_alpaca(params):
        Constructs and returns alpaca EH based on params.
    
    eh_binance(params):
        Constructs and returns binance EH based on params.
    
    eh_ibkr(params):
        Constructs and returns ibkr EH based on params.
    
    eh_alpha(params):
        Constructs and returns alpha EH based on params.
    
    .............................................................................................................
    """

    def __init__(self):
        return
    #--------------------------------------------------------------------------------------------------------------

    def construct_eh(self, enum, params):
        '''
        Constructs and returns proper EH based on passed in enum. 

            Parameters:
                enum (ENUM): enumeration for Execution Handler API (EH_api)
                params (list): contains Execution Handler (EH) parameters 
            
            Returns:
                Valid Execution Handler object based on parameter
            
            Throws:
                ValueError if parameter is invalid 
        '''
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
    #--------------------------------------------------------------------------------------------------------------

    def eh_alpaca(self, params):
        '''
        Constructs and returns alpaca EH based on params.

            Parameters:
                params (list): parameters for the alpaca api Data Handler 
            
            Returns:
                eh: valid alpaca Data Handler object
        '''
        eh = AlpacaExecutionHandler(params[0], params[1], params[2])
        return eh
    #--------------------------------------------------------------------------------------------------------------

    def eh_binance(self, params):
        '''
        Constructs and returns binance EH based on params

            Parameters:
                params (list): parameters for the binance api Execution Handler 
            
            Returns:
                Valid binance Execution Handler object 
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------

    def eh_ibkr(self, params):
        '''
        Constructs and returns ibkr EH based on params.

            Parameters:
                params (list): parameters for the ibkr api Exectuion Handler
            
            Returns: 
                Valid ibkr execution handler object 
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------

    def eh_alpha(self, params):
        '''
        Constructs and returns alpha EH based on params.

            Parameters:
                params (list): parameters for the alpha api Execution Handler
            
            Returns:
                Valid alpha Execution Handler object
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------
#==================================================================================================================

class Strategy_factory:

    # Overview: Class that creates and returns any Strategy object
    """
    Class: Strategy_factory
    .............................................................................................................

    Overview
    --------
    Class that creates and returns any Strategy object. 

    .............................................................................................................
    
    Attributes
    ----------
    N/A

    .............................................................................................................

    Methods
    -------
    construct_strat(enum, params):
        Constructs and returns proper startegy based on passed in enum.

    short_low_risk(params):
        Constructs and returns short_low_risk strat based on parameters.
    
    medium_low_risk(params):
        Constructs and returns medium_low_risk strat based on parameters.
    
    long_low_risk(params):
        Constructs and returns long_low_risk strat based on parameters.
    
    short_medium_risk(params):
        Constructs and returns short_medium_risk strat based on parameters.
    
    medium_medium_risk(params):
        Constructs and returns medium_medium_risk strat based on parameters.
    
    long_medium_risk(params):
        Constructs and returns long_medium_risk strat based on parameters.

    short_high_risk(params):
        Constructs and returns short_high_risk strat based on parameters.
    
    medium_high_risk(params):
        Constructs and returns medium_high_risk strat based on parameters.
    
    long_high_risk(params):
        Constructs and returns long_high_risk strat based on parameters.

    .............................................................................................................
    """
    def __init__(self):
        return
    #--------------------------------------------------------------------------------------------------------------

    def construct_strat(self, enum, params):
        """
        Constructs and returns proper startegy based on passed in enum.

            Parameterss:
                enum (ENUM): enumeration for the Strategy
                params (list): contains Strategy parameters

            Returns: 
                Valid Strategy object based on parameter
            
            Throws: 
                ValueError if parameter is invalid
        """
        if enum == 1:
            return self.short_low_risk(params)
        elif enum == 2:
            return self.medium_low_risk(params)
        elif enum == 3:
            return self.long_low_risk(params)
        elif enum == 4:
            return self.medium_low_risk(params)
        elif enum == 5:
            return self.medium_medium_risk(params)
        elif enum == 6:
            return self.long_medium_risk(params)
        elif enum == 7:
            return self.short_high_risk(params)
        elif enum == 8:
            return self.medium_high_risk(params)
        elif enum == 9:
            return self.long_high_risk(params)
        else:
            raise ValueError("Invalid ENUM")
    #--------------------------------------------------------------------------------------------------------------

    def short_low_risk(self, params):
        """
        Constructs and returns short_low_risk strat based on parameters.

            Parameters:     
                params (list): parameters for the short_low_risk strategy

            Returns: 
                Valid short_low_risk strategy object
        """
        strat = RL(params[0], params[1], params[2], params[3])
        return strat
    #--------------------------------------------------------------------------------------------------------------

    def medium_low_risk(self, params):
        """
        Constructs and returns medium_low_risk strat based on parameters.

            Parameters: 
                params (list): parameters for the medium_low_risk strategy

            Returns: 
                Valid medium_low_risk strategy object
        """
        strat = Strategy(1,params[0], params[1], params[2], params[3])
        return strat
    #--------------------------------------------------------------------------------------------------------------

    def long_low_risk(self, params):
        """
        Constructs and returns long_low_risk strat based on parameters.

            Parameters: 
                params (list): parameters for the long_low_risk strategy
            
            Returns: 
                Valid long_low_risk strategy object
        """
        strat = Strategy(2,params[0], params[1], params[2], params[3])
        return strat
    #--------------------------------------------------------------------------------------------------------------
    
    def short_medium_risk(self, params):
        """
        Constructs and returns short_medium_risk strat based on parameters.

            Parameters: 
                params (list): parameters for the short_medium_risk strategy

            Returns: 
                Valid short_medium_risk strategy object
        """
        strat = Strategy(3,params[0], params[1], params[2], params[3])
        return strat
    #--------------------------------------------------------------------------------------------------------------

    def medium_medium_risk(self, params):
        """
        Constructs and returns medium_medium_risk strat based on parameters.

            Parameters: 
                params (list): parameters for the medium_medium_risk strategy
            
            Returns: 
                Valid medium_medium_risk strategy object
        """
        strat = Strategy(4,params[0], params[1], params[2], params[3])
        return strat
    #--------------------------------------------------------------------------------------------------------------

    def long_medium_risk(self, params):
        """
        Constructs and returns long_medium_risk strat based on parameters.

            Paramseters: 
                params (list): parameters for the long_medium_risk strategy

            Returns: 
                Valid long_medium_risk strategy object
        """
        strat = Strategy(5,params[0], params[1], params[2], params[3])
        return strat
    #--------------------------------------------------------------------------------------------------------------
    
    def short_high_risk(self, params):
        """
        Constructs and returns short_high_risk strat based on parameters.

            Parameters: 
                params (list): parameters for the short_high_risk strategy

            Returns: 
                Valid short_high_risk strategy object
        """
        strat = Strategy(6,params[0], params[1], params[2], params[3])
        return strat
    #--------------------------------------------------------------------------------------------------------------

    def medium_high_risk(self, params):
        """
        Constructs and returns medium_high_risk strat based on parameters.

            Parameters: 
                params (list): parameters for the strategy

            Returns: 
                Valid medium_high_risk strategy object
        """
        strat = Strategy(7,params[0], params[1], params[2], params[3])
        return strat
    #--------------------------------------------------------------------------------------------------------------

    def long_high_risk(self, params):
        """
        Constructs and returns long_high_risk strat based on parameters.

            Parameters: 
                params (list): parameters for the long_high_risk strategy

            Returns: 
                Valid long_high_risk strategy object
        """
        strat = Strategy(8,params[0], params[1], params[2], params[3])
        return strat
    #--------------------------------------------------------------------------------------------------------------
#==================================================================================================================