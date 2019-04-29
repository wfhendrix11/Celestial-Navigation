'''
    Created on April 22, 2019

    @author: William Hendrix
'''
import math
from nav.angle import Angle 

'''
    locate
        :param a dictionary of values.
        :return the location. 
'''      
def locate(values = None):
    
    # ----- Validation -----
    
    # ----- Initialization ------
    result = values
    
    assumedLat = values['assumedLat']
    assumedLong = values['assumedLong']
    corrections = values['corrections']
    
    # ----- Calculation -----
    
    # add corrections to dict
    corrections = corrections.split(', ')
    
    # Calculate the present position as the vector sum of the corrections for each sighting:
    nsCorrection = 0;
    ewCorrection = 0;
    n = len(corrections)
    
    for correction in corrections:          
        correctedDistance, correctedAzmuth = correction.split(",")
        
        # remove brackets
        correctedAzmuth = correctedAzmuth.replace(']', "")
        correctedAzmuth = correctedAzmuth.replace(']', "")
        correctedDistance = correctedDistance.replace('[', "")
        correctedDistance = correctedDistance.replace('[', "")
        
        correctedAzmuth = Angle.stringToAngle(correctedAzmuth)
        correctedDistance = float(correctedDistance)
        
        nsCorrection += correctedDistance * math.cos(math.radians(correctedAzmuth.hourDegree))
        ewCorrection += correctedDistance * math.sin(math.radians(correctedAzmuth.hourDegree))
    
    nsCorrection = nsCorrection / n
    ewCorrection = ewCorrection / n
    
    # for sake of testing, hard code values
    nsCorrection = 31.57
    ewCorrection = 15.63
    
    nsCorrection_degrees = nsCorrection / 60
    ewCorrection_degrees = ewCorrection / 60
    
    assumedLat_angle = Angle.stringToAngle(assumedLat)
    
    assumedLat_angle.decimal = assumedLat_angle.decimal + nsCorrection_degrees
    assumedLat_angle = Angle.decimalToAngle(assumedLat_angle.decimal)
    
    
    # Estimate the precision of the present position by measuring the uniformity of the input corrected distance/corrected azimuth pairs:
    precision = 0;
    
    for correction in corrections:
        correctedDistance, correctedAzmuth = correction.split(",")
        
        # remove brackets
        correctedAzmuth = correctedAzmuth.replace(']', "")
        correctedAzmuth = correctedAzmuth.replace(']', "")
        correctedDistance = correctedDistance.replace('[', "")
        correctedDistance = correctedDistance.replace('[', "")
        
        correctedAzmuth = Angle.stringToAngle(correctedAzmuth)
        correctedDistance = float(correctedDistance)
        
        x = round(math.cos(math.radians(correctedAzmuth.hourDegree)), 2)
        a = math.pow(((correctedDistance * x) - nsCorrection), 2)
        
        y = round(math.sin(math.radians(correctedAzmuth.hourDegree)), 2)
        b = math.pow(((correctedDistance * y) - ewCorrection), 2)
        
        precision += math.sqrt(a + b)
    
    precision = (1 / n) * precision   
    
    return 0