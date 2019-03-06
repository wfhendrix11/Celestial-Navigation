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
        Input: year, month, day, hour, minute, seconds
        Output: an adjusted dictionary of values
    ''' 
    def getGreenwich(self, year, month, day, hour, minute, second):
        