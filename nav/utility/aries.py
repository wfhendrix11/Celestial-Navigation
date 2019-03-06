'''
Created on March 1, 2018

@author: William Hendrix
'''

from datetime import datetime, timedelta
import math
from angle import Angle

class Aries:
    
    '''
    getGreenwich
        Input: year, month, day, hour, minute, seconds
        Output: an adjusted dictionary of values
    ''' 
    def getGreenwich(self, year, month, day, hour, minute, second):
        referenceDatetime_string = str(year) + ",01,01,00,00,00"
        observationDatetime_string = str(year) + ',' + str(month) + ',' + str(day) + ','
        observationDatetime_string += str(hour) + ',' + str(minute) + ',' + str(second)
        
        observationDatetime = datetime.strptime(observationDatetime_string, '%Y,%m,%d,%H,%M,%S')
        referenceDatetime = datetime.strptime(referenceDatetime_string, '%Y,%m,%d,%H,%M,%S')
        secongs_since_reference = (observationDatetime - referenceDatetime).total_seconds()
        
        relative_pm = Aries.__get_relative_prime_meridian(year)
        earth_rotation = Aries.__get_earth_rotation_since_observation(secongs_since_reference)
        
        print("relative_pm" + relative_pm.str)
        print("earth_rotation" + earth_rotation.str)
        return Angle.add(relative_pm, earth_rotation)
    
    def getPrimeMeridian(self, year):
        referenceRotation = Angle.from_string("100d42.6")
        
        # cumulative progression: delta(year-2001) * -0d14.31667
        annual_gha_decrement = Angle.from_string("-0d14.32")
        delta_year = year - Aries.REFERENCE_YEAR
        cumulative_progression = Angle.multiply(annual_gha_decrement, delta_year)
        
        # leap progression: (leap years elapsed) * 0d59.0
        daily_rotation = Angle.from_string("0d59.0")
        leap_years = math.floor((year - Aries.REFERENCE_YEAR)/4)
        leap_progression = Angle.multiply(daily_rotation, leap_years)
        
        # total progression = 100d42.6 + cumulative prog + leap progs
        
        total_progression = Angle.add(reference_rotation, cumulative_progression)
        total_progression = Angle.add(total_progression, leap_progression)
        print("total progression" + total_progression.str)
        return total_progression