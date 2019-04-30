'''
    Created on April 22, 2019

    @author: William Hendrix
'''

import unittest
import nav.locate as nav
import httplib
from urllib import urlencode
import json

class locateTest(unittest.TestCase):

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
    # 100 correct operation
    #   Happy path analysis:
    #        values:      mandatory
    #                     dictionary
    #                     Operations:   {'op':'locate'}
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
    
    def test100_010ShouldReturnChangedValuesWithOperationLocate(self):   
        # Arrange
        correctDict = {'op':'locate', 'assumedLat':'32d36.5', 'assumedLong':'274d31.1', 
                       'presentLat':'33d8.1','presentLong':'274d46.7','precision':'45','accuracy':'NA', 
                       'corrections': '[[50,45d0.0], [75,60d42.0], [100,300d11.2], [42,42d12.3], [70,60d45.0], [10,280d0.0]]'}        
               
        self.setParm('op','locate')
        self.setParm('assumedLat','32d36.5')
        self.setParm('assumedLong','274d31.1')
        self.setParm('corrections','[[50,45d0.0], [75,60d42.0], [100,300d11.2], [42,42d12.3], [70,60d45.0], [10,280d0.0]]')  
                 
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                 
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test100_020ShouldReturnChangedValuesWithOperationLocate(self):   
        # Arrange
        correctDict = {'op':'locate', 'assumedLat':'-53d38.4', 'assumedLong':'350d35.3', 
                       'presentLat':'-50d41.6','presentLong':'350d37.0','precision':'0','accuracy':'NA', 
                       'corrections': '[[100,1d0.0]]'}        
                
        self.setParm('op','locate')
        self.setParm('assumedLat','-53d38.4')
        self.setParm('assumedLong','350d35.3')
        self.setParm('corrections','[[100,1d0.0]]')  
                  
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                  
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
    
    # --------------------- Sad path ---------------------
    
    def test200_010ShouldReturnMissingAssumedLat(self):
        # Arrange
        correctDict = {'error': 'mandatory information missing'}        
                
        self.setParm('op','locate')
        #self.setParm('assumedLat','-53d38.4')
        self.setParm('assumedLong','350d35.3')
        self.setParm('corrections','[[100,1d0.0]]')  
                  
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                  
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test200_020ShouldReturnMissingAssumedLong(self):
        # Arrange
        correctDict = {'error': 'mandatory information missing'}        
                
        self.setParm('op','locate')
        self.setParm('assumedLat','-53d38.4')
        #self.setParm('assumedLong','350d35.3')
        self.setParm('corrections','[[100,1d0.0]]')  
                  
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                  
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test200_030ShouldReturnMissingCorrections(self):
        # Arrange
        correctDict = {'error': 'mandatory information missing'}        
                
        self.setParm('op','locate')
        self.setParm('assumedLat','-53d38.4')
        self.setParm('assumedLong','350d35.3')
        #self.setParm('corrections','[[100,1d0.0]]')  
                  
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                  
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test100_040ShouldReturnAssumedLatTooBig(self):   
        # Arrange
        correctDict = {'error': 'assumedLat is invalid'}        
                
        self.setParm('op','locate')
        self.setParm('assumedLat','91d0.0')
        self.setParm('assumedLong','350d35.3')
        self.setParm('corrections','[[100,1d0.0]]')  
                  
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                  
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test100_041ShouldReturnAssumedLatTooSmall(self):   
        # Arrange
        correctDict = {'error': 'assumedLat is invalid'}        
                
        self.setParm('op','locate')
        self.setParm('assumedLat','-91d0.0')
        self.setParm('assumedLong','350d35.3')
        self.setParm('corrections','[[100,1d0.0]]')  
                  
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                  
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test100_050ShouldReturnAssumedLongTooBig(self):   
        # Arrange
        correctDict = {'error': 'assumedLong is invalid'}        
                
        self.setParm('op','locate')
        self.setParm('assumedLat','32d36.5')
        self.setParm('assumedLong','361d35.3')
        self.setParm('corrections','[[100,1d0.0]]')  
                  
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                  
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test100_051ShouldReturnAssumedLongTooSmall(self):   
        # Arrange
        correctDict = {'error': 'assumedLong is invalid'}        
                
        self.setParm('op','locate')
        self.setParm('assumedLat','32d36.5')
        self.setParm('assumedLong','-1d35.3')
        self.setParm('corrections','[[100,1d0.0]]')  
                  
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                  
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)      