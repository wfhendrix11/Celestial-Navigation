'''
    Created on February 18, 2018

    @author: William Hendrix
'''

import unittest
import nav.adjust as nav
import httplib
from urllib import urlencode
import json

class adjustTest(unittest.TestCase):

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
    # 100 adjust operation
    #   Happy path analysis:
    #        values:      mandatory
    #                     dictionary
    #                     Operations:   {'op':'adjust'}
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

#     def test100_010ShouldReturnChangedValuesWithOperationAdjust(self):   
#         # Arrange
#         correctDict = {'altitude':'29d59.9', 'observation': '30d1.5', 'height': '19.0',
#                        'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
#         self.setParm('observation', '30d1.5')
#         self.setParm('height', '19.0')
#         self.setParm('pressure', '1000')
#         self.setParm('horizon', 'artificial')
#         self.setParm('op','adjust')
#         self.setParm('temperature', '85')
#          
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#          
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#      
#     def test100_020ShouldReturnChangedValuesWithOperationAdjust(self):   
#         # Arrange
#         correctDict = {'altitude':'45d11.9', 'observation': '45d15.2', 'height': '6', 
#                        'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
#         self.setParm('observation', '45d15.2')
#         self.setParm('height', '6')
#         self.setParm('pressure', '1010')
#         self.setParm('horizon', 'natural')
#         self.setParm('op','adjust')
#         self.setParm('temperature', '71')
#          
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#          
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#          
#     def test100_030ShouldReturnChangedValuesWithOperationAdjustOnlyObservation(self):
#         # Arrange
#         correctDict = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust'}  
#         self.setParm('observation', '42d0.0')
#         self.setParm('op','adjust')
#          
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#          
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#          
#     def test100_040ShouldReturnChangedValuesWithOperationAdjustExtraKey(self):
#         # Arrange 
#         correctDict = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust',
#                        'extraKey':'ignore'}
#         self.setParm('observation', '42d0.0')
#         self.setParm('op','adjust')
#         self.setParm('observation', '42d0.0')
#         self.setParm('extraKey','ignore')  
#          
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#          
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#      
#     def test100_050ShouldReturnChangedValuesWithOperationAdjustNoPressure(self):   
#         # Arrange
#         correctDict = {'altitude':'29d59.9', 'observation': '30d1.5', 'height': '19.0',
#                        'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
#         self.setParm('observation', '30d1.5')
#         self.setParm('height', '19.0')
#         self.setParm('horizon', 'artificial')
#         self.setParm('op','adjust')
#         self.setParm('temperature', '85')    
#                  
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#          
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#      
#     def test100_060ShouldReturnChangedValuesWithOperationAdjustNoHeight(self):   
#         # Arrange
#         correctDict = {'altitude':'29d59.9', 'observation': '30d1.5',
#                        'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
#         self.setParm('observation', '30d1.5')
#         self.setParm('pressure', '1000')
#         self.setParm('horizon', 'artificial')
#         self.setParm('op','adjust')
#         self.setParm('temperature', '85')
#          
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#          
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#          
#     def test100_070ShouldReturnChangedValuesWithOperationAdjustNoTemperature(self):   
#         # Arrange
#         correctDict = {'altitude':'29d59.9', 'observation': '30d1.5', 'height': '19.0',
#                        'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust'}
#         self.setParm('observation', '30d1.5')
#         self.setParm('height', '19.0')
#         self.setParm('pressure', '1000')
#         self.setParm('horizon', 'artificial')
#         self.setParm('op','adjust')
#          
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#          
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)    
#          
#     def test100_080ShouldReturnChangedValuesWithOperationAdjustNoHorizon(self):   
#         # Arrange
#         correctDict = {'observation': '30d1.5', 'altitude': '29d55.7', 'height': '19.0',
#                        'pressure': '1000', 'op': 'adjust', 'temperature': '85'}
#         self.setParm('observation', '30d1.5')
#         self.setParm('height', '19.0')
#         self.setParm('pressure', '1000')
#         self.setParm('op','adjust')
#         self.setParm('temperature', '85')
#          
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#          
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)  
#         
#     # --------------------- Sad path ---------------------  
#     
#     def test100_910ShouldReturnNoObservationProvided(self):
#         # Arrange
#         correctDict = {'error': 'no observation provided'}  
#         self.setParm('op','adjust')
#           
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#           
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#          
#     def test100_920ShouldReturnXInvalidTooLarge(self):
#         # Arrange
#         correctDict = {'error': 'x is invalid'}  
#         self.setParm('observation', '100d1.5')
#         self.setParm('op','adjust')
#            
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#            
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#      
#     def test100_925ShouldReturnXInvalidTooSmall(self):
#         # Arrange
#         correctDict = {'error': 'x is invalid'}  
#         self.setParm('observation', '-1d1.5')
#         self.setParm('op','adjust')
#            
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#            
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#  
#     def test100_930ShouldReturnYInvalidTooLarge(self):
#         # Arrange
#         correctDict = {'error': 'y is invalid'}  
#         self.setParm('observation', '30d61')
#         self.setParm('op','adjust')
#             
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#             
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)      
#      
#     def test100_935ShouldReturnYInvalidTooSmall(self):
#         # Arrange
#         correctDict = {'error': 'y is invalid'}  
#         self.setParm('observation', '30d-1')
#         self.setParm('op','adjust')
#             
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#             
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#     
#     def test100_945ShouldReturnHeightLessThanZero(self):
#         # Arrange
#         correctDict = {'error': 'height must be greater than 0'}  
#         self.setParm('observation', '30d1.5')
#         self.setParm('height', '-1')
#         self.setParm('op','adjust')
#              
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#              
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)

    def test100_950ShouldReturnPressureInvalid(self):
        # Arrange
        correctDict = {'error': 'pressure is invalid'}  
        self.setParm('observation', '30d1.5')
        self.setParm('pressure', '90')
        self.setParm('op','adjust')
              
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
              
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    def test100_955ShouldReturnPressureInvalid(self):
        # Arrange
        correctDict = {'error': 'pressure is invalid'}  
        self.setParm('observation', '30d1.5')
        self.setParm('pressure', '1200')
        self.setParm('op','adjust')
              
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
              
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)

        
        
        