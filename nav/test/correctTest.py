'''
    Created on March 27, 2019

    @author: William Hendrix
'''

import unittest
import nav.correct as nav
import httplib
from urllib import urlencode
import json

class correctTest(unittest.TestCase):

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
    #                     Operations:   {'op':'correct'}
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
    
#     def test100_010ShouldReturnChangedValuesWithOperationCorrect(self):   
#         # Arrange
#         correctDict = {'assumedLat': '53d38.4', 'correctedDistance': 104, 'altitude': '13d42.3', 
#                        'assumedLong': '350d35.3', 'long': '95d41.6', 'lat': '16d32.3', 
#                        'correctedAzimuth': '262d55.6', 'op': 'correct'}
#              
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')  
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3')  
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
#     def test200_010ShouldReturnMandatoryInformationMissing(self):
#         # Arrange
#         correctDict = {'error': 'mandatory information missing'}
#              
#         self.setParm('op','correct')
#                
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#                
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#          
#     def test200_011ShouldReturnMandatoryInformationMissing_Lat(self):
#         # Arrange
#         correctDict = {'error': 'mandatory information missing'}
#              
#         self.setParm('op','correct')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3') 
#                
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#                
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#  
#     def test200_012ShouldReturnMandatoryInformationMissing_Long(self):
#         # Arrange
#         correctDict = {'error': 'mandatory information missing'}
#              
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3') 
#                
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#                
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#          
#     def test200_013ShouldReturnMandatoryInformationMissing_Altitude(self):
#         # Arrange
#         correctDict = {'error': 'mandatory information missing'}
#              
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3') 
#                
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#                
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#         
#     def test200_014ShouldReturnMandatoryInformationMissing_AssumedLat(self):
#         # Arrange
#         correctDict = {'error': 'mandatory information missing'}
#              
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLong','350d35.3') 
#                
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#                
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
#        
#     def test200_015ShouldReturnMandatoryInformationMissing_AssumedLong(self):
#         # Arrange
#         correctDict = {'error': 'mandatory information missing'}
#             
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4') 
#               
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#               
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)
# 
#     def test200_020ShouldReturnInvalidLat(self):
#         # Arrange
#         correctDict = {'error': 'lat is invalid'}
#              
#         self.setParm('op','correct')
#         self.setParm('lat','200d32.3')  
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3')  
#                
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#                
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)

#     def test200_030ShouldReturnInvalidAssumedLat(self):
#         # Arrange
#         correctDict = {'error': 'assumedLat is invalid'}
#               
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')  
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','200d38.4')
#         self.setParm('assumedLong','350d35.3')  
#                 
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#                 
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)

#     def test200_040ShouldReturnInvalidLong(self):
#         # Arrange
#         correctDict = {'error': 'long is invalid'}
#               
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')  
#         self.setParm('long','400d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3')  
#                 
#         # Act
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#                 
#         # Assert
#         self.assertDictEqual(correctDict, resultDictionary)

    def test200_050ShouldReturnInvalidAssumedLong(self):
        # Arrange
        correctDict = {'error': 'assumedlong is invalid'}
              
        self.setParm('op','correct')
        self.setParm('lat','16d32.3')  
        self.setParm('long','95d41.6')
        self.setParm('altitude','13d42.3')
        self.setParm('assumedLat','53d38.4')
        self.setParm('assumedLong','450d35.3')  
                
        # Act
        result = self.microservice()
        resultDictionary = self.string2dict(result)
                
        # Assert
        self.assertDictEqual(correctDict, resultDictionary)
        
    