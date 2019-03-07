'''
    Created on March 1, 2018

    @author: William Hendrix
'''

import unittest
import nav.predict as nav
import httplib
from urllib import urlencode
import json

class predictTest(unittest.TestCase):

    def setUp(self):
        self.inputDictionary = {}
        self.errorKey = "error"
        self.solutionKey = "probability"
        self.BX_PATH = '/nav?'
        self.BX_PORT = 5000
        self.BX_URL = 'localhost'

    def tearDown(self):
        self.inputDictionary = {}

    def setParm(self, key, value):
        self.inputDictionary[key] = value

    def microservice(self):
        try:
            theParm = urlencode(self.inputDictionary)
            theConnection = httplib.HTTPConnection(self.BX_URL, self.BX_PORT)
            theConnection.request("GET", self.BX_PATH + theParm)
            theStringResponse = theConnection.getresponse().read()
            return theStringResponse
        except Exception as e:
            return "error encountered during transaction"

    def string2dict(self, httpResponse):
        '''Convert JSON string to dictionary'''
        result = {}
        try:
            jsonString = httpResponse.replace("'", "\"")
            unicodeDictionary = json.loads(jsonString)
            for element in unicodeDictionary:
                if(isinstance(unicodeDictionary[element],unicode)):
                    result[str(element)] = str(unicodeDictionary[element])
                else:
                    result[str(element)] = unicodeDictionary[element]
        except Exception as e:
            result['diagnostic'] = str(e)
        return result    

# -----------------------------------------------------------------------
    # ---- Acceptance Tests
    # 100 predict operation
    #   Happy path analysis:
    #        values:      mandatory
    #                     dictionary
    #                     Operations:   {'op':'predict'}
    #                      
    #   Sad path analysis:
    #        values:
    #                     no op specified             values={}
    #                        -- return {'error':'no op  is specified'}
    #                     contain 'error' as a key      values={5d04.9', 'height': '6.0', 'pressure': '1010',
    #                                                           'horizon': 'artificial', 'temperature': '72'
    #                                                           'error':'no op is specified'}'
    #                        -- return values without error as a key and without its values
    #                     not-dictionary                values=42
    #                        -- return {'error':'parameter is not a dictionary'}
    #                     not legal operation           values={'op': 'unknown'}
    #                        -- return {'error':'op is not a legal operation'}
    #                     missing dictionary            dispatch()
    #                        -- return {'error':'dictionary is missing'}
    
    # --------------------- Happy path ---------------------
 
    def test100_010ShouldReturnChangedValuesWithOperationPredict(self):   
        # Arrange
        correctDict = {'op':'predict', 'body': 'Aldebaran', 'date': '2016-01-17',
                       'time': '03:15:42', 'long':'95d41.5', 'lat':'16d32.3'}
            
        self.setParm('op','predict')
        self.setParm('body','Aldebaran')  
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42') 
              
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
              
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test100_020ShouldReturnChangedValuesWithOperationPredict(self):   
        # Arrange
        correctDict = {'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17',
                       'time': '03:15:42', 'long':'75d53.5', 'lat':'7d24.3'}
             
        self.setParm('op','predict')
        self.setParm('body','Betelgeuse')  
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42') 
               
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
               
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
          
    # --------------------- Sad path ---------------------     
            
    def test200_010ShouldReturnNoBody(self):
        # Arrange
        correctDict = {'error':'no body provided'}
             
        self.setParm('op','predict')
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42') 
               
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
               
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
           
    def test200_020ShouldReturnUnknownStar(self):
        # Arrange
        correctDict = {'error':'unknown star'}
            
        self.setParm('op','predict')
        self.setParm('body','unknown') 
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42') 
              
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
              
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
          
    def test200_030ShouldReturnInvalidDate(self):
          
        # Arrange
        correctDict = {'error':'invalid date'}
             
        self.setParm('op','predict')
        self.setParm('body','Betelgeuse')  
        self.setParm('date','1990-01-17')
        self.setParm('time','03:15:42') 
               
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
               
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)    
                       
    def test200_040ShouldReturnInvalidTimeHour(self):
     
        # Arrange
        correctDict = {'error':'invalid time'}
            
        self.setParm('op','predict')
        self.setParm('body','Betelgeuse')  
        self.setParm('date','2016-01-17')
        self.setParm('time','25:15:42') 
              
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
              
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test200_041ShouldReturnInvalidTimeMinute(self):
    
        # Arrange
        correctDict = {'error':'invalid time'}
           
        self.setParm('op','predict')
        self.setParm('body','Betelgeuse')  
        self.setParm('date','2016-01-17')
        self.setParm('time','03:70:42') 
             
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
             
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test200_042ShouldReturnInvalidTimeSecond(self):
    
        # Arrange
        correctDict = {'error':'invalid time'}
           
        self.setParm('op','predict')
        self.setParm('body','Betelgeuse')  
        self.setParm('date','2016-01-17')
        self.setParm('time','03:02:70') 
             
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
             
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)         
        
        