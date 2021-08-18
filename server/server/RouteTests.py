from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from passlib.hash import pbkdf2_sha256
from database.UsersTest import *

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
    def RunTests():
    '''
    Runs all the testing functions sequentially

        Parameters:
            
        
        Returns: 
            
    '''
    #--------------------------------------------------------------------------------------------------------------
    def TestLogin():
    '''
    Tests that the login route function works properly by adding something to the database and then ensureing that
    its there.

        Parameters:
            none.
        
        Returns: 
            none.
    '''

    #--------------------------------------------------------------------------------------------------------------
    def TestRegister():
    '''
    Tests that the register route works properly by using the register function to register a new user and ensureing that 
    it was added to the database properly.

        Parameters:
            none.
        
        Returns: 
            none.
            
    '''
    #--------------------------------------------------------------------------------------------------------------
    def TestID():
    '''
    Adds a new user to the data base uses the function to retrive the ID we registered and ensures that it worked.

        Parameters:
            none.
        
        Returns: 
            none.
            
    '''
        
    #--------------------------------------------------------------------------------------------------------------
    def TestGetBotInfoWithID():
    '''
    Registers a new User with specfifc user ID then calls the function to grab the ID and ensures that the Info 
    retuned is the same as what we constructed it with.

        Parameters:
            none.
        
        Returns: 
            none.
    '''
        
    #--------------------------------------------------------------------------------------------------------------
    def TestGetBotInfo():
    '''
    Registers a new user and tests that the info the new user was constructed with is correct with the info retrived.

        Parameters:
            none.
        
        Returns: 
            none.
    '''

    #--------------------------------------------------------------------------------------------------------------