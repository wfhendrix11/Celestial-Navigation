'''
Created on March 1, 2018

@author: William Hendrix
'''

from datetime import datetime, timedelta
import math
from nav.angle import Angle

class Aries:
    
    '''
    getGreenwich
        :params year, month, day, hour, minute, seconds
        :return an adjusted dictionary of values
    '''
    @classmethod 
    def getGreenwichHourAngle(year, month, day, hour, minute, second):
        
        