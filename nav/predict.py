'''
    Created on March 1, 2018

    @author: William Hendrix
'''

import math
from nav.stars import STARS
from nav.angle import Angle
from nav.aries import Aries

'''
    Predict
        :param a dictionary of values
        :return a prediction of dictionary of values
'''      
def predict(values = None):
    
    # ------ Initialization ------
    result = values
    
    body = values['body']
    
    if 'date' in values:
        date = values['date']
    else: 
        date = '2001-01-01'
    
    if 'time' in values:
        time = values['time']
    else:
        time = "00:00:00"
    
    sidereal = STARS[body]['sidereal']
    
    declination = STARS[body]['declination']
    
    # ------ Calculation ------
    latitude = Angle.stringToAngle(declination)
    (year, month, day) = date.split("-")
    (hour, minute, second) = time.split(":")
    year = int(year)
    month = int(month)
    day = int(day)
    hour = int(hour)
    minute = int(minute)
    second = int(second)
    
    gha = Aries.getGreenwichHourAngle(year, month, day, hour, minute, second)
    sha = Angle.stringToAngle(sidereal)
    
    longitude = Angle.add(gha, sha)
    fullAngle = Angle.stringToAngle("-360d0.0")
    
    if longitude.hourDegree > 360:
        longitude = Angle.add(longitude, fullAngle)
        
    if longitude.hourDegree == 360 and longitude.minuteDegree > 0:
        longitude = Angle.add(longitude, fullAngle)
        
    result['lat'] = latitude.str
    result['long'] = longitude.str
    
    return result
