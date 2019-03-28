'''
    Created on March 27, 2019

    @author: William Hendrix
'''
import math
from nav.angle import Angle

'''
    correct
        :param a dictionary of values.
        :return the difference between the observed and expected angle. 
'''      
def correct(values = None):
    
    # ----- Validation -----
    if values is None or not isinstance(values, dict):
        return {'error': 'values is not provided'}
    
    if (not('lat' in values)):
        return {'error': 'mandatory information missing'}
    if (not('long' in values)):
        return {'error': 'mandatory information missing'}
    if (not('altitude' in values)):
        return {'error': 'mandatory information missing'}
    if (not('assumedLat' in values)):
        return {'error': 'mandatory information missing'}
    if (not('assumedLong' in values)):
        return {'error': 'mandatory information missing'}
    
    # validate lat
    
    # ----- Initialization -----
    result = values
    
    lat = values['lat']
    longitude = values['long']
    altitude = values['altitude']
    assumedLat = values['assumedLat']
    assumedLong = values['assumedLong']
    
    # ----- Calculation -----
    lat = Angle.stringToAngle(lat)
    longitude = Angle.stringToAngle(longitude)
    assumedLat = Angle.stringToAngle(assumedLat)
    assumedLong = Angle.stringToAngle(assumedLong)
    altitude = Angle.stringToAngle(altitude)
    
    # calculate the local hour angle of the navigator
    lha = Angle.add(longitude, assumedLong)
    
    # calculate the angle to adjust the observed altitude to match 
    # the star observed from the assumed position
    sin_lat = math.sin(math.radians(lat.decimal * 360))
    cos_lat = math.cos(math.radians(lat.decimal * 360))
    
    sin_assumedLat = math.sin(math.radians(assumedLat.decimal * 360))
    cos_assumedLat = math.cos(math.radians(assumedLat.decimal * 360))
    cos_lha = math.cos(math.radians(lha.decimal * 360))
    
    intermediateDistance = sin_lat * sin_assumedLat + cos_lat * cos_assumedLat * cos_lha
    
    correctedAltitude = math.asin(intermediateDistance) / math.pi * 180 / 360
    correctedAltitude = Angle.decimalToAngle(-correctedAltitude)
    
    # Calculate the distance the navigator needs to move to make the 
    # observed and calculated star positions match 
    correctedDistance = Angle.add(altitude, correctedAltitude)
    correctedDistance = int(correctedDistance.decimal * 60 * 360)
    
    # Determine the compass direction in which to make the distance adjustment
    compassDirection = math.cos(math.radians(correctedAltitude.decimal * 360))
    
    numerator = (sin_lat - (sin_assumedLat * intermediateDistance))
    denomonator = cos_assumedLat * compassDirection
    
    correctedAz = math.acos(numerator / denomonator)
    correctedAzDegree = math.degrees(correctedAz)
    correctedAzimuth = Angle.decimalToAngle(correctedAzDegree / 360)
    
    # If the correctedDistance < 0, then normalize  by 1) obtaining the absolute value of the 
    # correctedDistance and 2) adjusting the correctedAzimuth by 180 degrees
    if (correctedDistance < 0):
        correctedDistance = abs(correctedDistance) + 1
        correctedAzimuth.str = str(correctedAzimuth.hourDegree + 180) + "d" + str(correctedAzimuth.minuteDegree)
        
    result['correctedDistance'] = correctedDistance
    result['correctedAzimuth'] = correctedAzimuth.str
    
    return result
    
    
    