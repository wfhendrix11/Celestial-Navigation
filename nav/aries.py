'''
Created on March 1, 2018

@author: William Hendrix
'''

from datetime import datetime, timedelta
import math
from nav.angle import Angle

class Aries:
    
    '''
    getGreenwichHourAngle
        :params year, month, day, hour, minute, seconds
        :return an adjusted dictionary of values
    '''
    @classmethod 
    def getGreenwichHourAngle(cls, year, month, day, hour, minute, second):
        
        referenceDatetime = str(year) + ",01,01,00,00,00"
        observationDatetime = str(year) + ',' + str(month) + ',' + str(day) + ','
        observationDatetime += str(hour) + ',' + str(minute) + ',' + str(second)
        
        observationDatetime = datetime.strptime(observationDatetime, '%Y,%m,%d,%H,%M,%S')
        referenceDatetime = datetime.strptime(referenceDatetime, '%Y,%m,%d,%H,%M,%S')
        secondsSinceReference = (observationDatetime - referenceDatetime).total_seconds()
        
        relativePrimeMeridian = Aries.getPrimeMeridian(year)
        earthRotation = Aries.getEarthRotationSinceObservation(secondsSinceReference)
        
        return Angle.add(relativePrimeMeridian, earthRotation)
        
    '''
    getPrimeMeridian
        :params year
        :return total progression
    '''    
    @classmethod
    def getPrimeMeridian(cls, year):
        
        referenceRotation = Angle.stringToAngle("100d42.6")
        yearlyGHADecrement = Angle.stringToAngle("-0d14.32")
        deltaYear = year - 2001
        cumulativeProgression = Angle.multiply(yearlyGHADecrement, deltaYear)
        
        dailyRotation = Angle.stringToAngle("0d59.0")
        leapYears = math.floor((year - 2001) / 4)
        leapProgression = Angle.multiply(dailyRotation, leapYears)
        
        totalProgression = Angle.add(referenceRotation, cumulativeProgression)
        totalProgression = Angle.add(totalProgression, leapProgression)
        
        return totalProgression
    
    '''
    getEarthRotationSinceObservation
        :params elapsed seconds
        :return total rotation
    '''
    @classmethod
    def getEarthRotationSinceObservation(cls, elapsedSeconds):
        rotation = round(elapsedSeconds)
        
        return Angle.decimalToAngle(rotation)
        
        