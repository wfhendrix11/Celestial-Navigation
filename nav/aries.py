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
    def getGreenwichHourAngle(year, month, day, hour, minute, second):
        
        referenceDatetime = str(year) + ",01,01,00,00,00"
        observationDatetime = str(year) + ',' + str(month) + ',' + str(day) + ','
        observationDatetime += str(hour) + ',' + str(minute) + ',' + str(second)
        
        observationDatetime = datetime.strptime(observationDatetime, '%Y,%m,%d,%H,%M,%S')
        referenceDatetime = datetime.strptime(referenceDatetime, '%Y,%m,%d,%H,%M,%S')
        secondsSinceReference = (observationDatetime - referenceDatetime).total_seconds()
        
        relativePrimeMeridian = Aries.getPrimeMeridian(year)
        
    '''
    getPrimeMeridian
        :params year
        :return total progression
    '''    
    @classmethod
    def getPrimeMeridian(cls, year):
    
        return 0
        
        