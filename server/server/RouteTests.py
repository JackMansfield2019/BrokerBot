import json

class RouteTests:
    """
    Class: RouteTests

    .............................................................................................................

    Overview
    --------
    runs tests on The route functions. 

    .............................................................................................................
    
    Attributes
    ----------
    

    .............................................................................................................

    Methods
    -------
    RunTests:
        runs all the tests sequntially
    
    TestLogin:
        tests the login routing funciton
    
    TestRegister:
        tests the register routing funciton
    
    TestID:
        tests the ID routing funciton
    
    TestGetBotInfoWithID:
        tests the GetBotInfoWithID routing funciton to ensure that it returns correct information.
    
    TestGetBotInfo:
        tests the GetBotInfoWithID routing funciton to ensure that it returns correct information.
    
    .............................................................................................................

    Extra Information
    -----------------
    .............................................................................................................
    """
    #--------------------------------------------------------------------------------------------------------------
    
    
    def __init__(self):
        '''
        Runs all the testing functions sequentially

            Parameters:
                none
            
            Returns: 
                none
        '''
        self.TestLogin()
        self.TestRegister()
        self.TestID()
        self.TestGetBotInfoWithID()
        self.TestGetBotInfo()
    #--------------------------------------------------------------------------------------------------------------
    def TestLogin(self):
        '''
        Tests that the login route function works properly by adding something to the database and then ensureing that
        its there.

            Parameters:
                none.
            
            Returns: 
                none.
        '''
        print(".TEST   TestLogin [VALID REGISTRATION] ...", end = ' ')
        print("FAILED")
    #--------------------------------------------------------------------------------------------------------------
    def TestRegister(self):
        '''
        Tests that the register route works properly by using the register function to register a new user and ensureing that 
        it was added to the database properly.

            Parameters:
                none.
            
            Returns: 
                none.   
        '''
        print(".TEST   TestRegister [VALID REGISTRATION] ...", end = ' ')
        print("FAILED")
    #--------------------------------------------------------------------------------------------------------------
    def TestID(self):
        '''
        Adds a new user to the data base uses the function to retrive the ID we registered and ensures that it worked.

            Parameters:
                none.
            
            Returns: 
                none.
                
        '''
        print(".TEST   TestRegister [VALID ID] ...", end = ' ')
        print("FAILED")
    #--------------------------------------------------------------------------------------------------------------
    def TestGetBotInfoWithID(self):
        '''
        Registers a new User with specfifc user ID then calls the function to grab the ID and ensures that the Info 
        retuned is the same as what we constructed it with.

            Parameters:
                none.
            
            Returns: 
                none.
        '''
        print(".TEST   TestGetBotInfoWithID [VALID INFORMATION] ...", end = ' ')
        print("FAILED")
    #--------------------------------------------------------------------------------------------------------------
    def TestGetBotInfo(self):
        '''
        Registers a new user and tests that the info the new user was constructed with is correct with the info retrived.

            Parameters:
                none.
            
            Returns: 
                none.
        '''
        print(".TEST   TestGetBotInfo [VALID INFORMATION] ...", end = ' ')
        print("FAILED")
    #--------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    tests = RouteTests()
