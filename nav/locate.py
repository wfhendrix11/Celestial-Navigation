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
        correctedAzmuth.decimal = correctedAzmuth.hourDegree + (correctedAzmuth.minuteDegree / 60)
        correctedDistance = float(correctedDistance)
        
        nsCorrection += correctedDistance * math.cos(math.radians(correctedAzmuth.decimal))
        ewCorrection += correctedDistance * math.sin(math.radians(correctedAzmuth.decimal))
    
    nsCorrection = nsCorrection / n
    ewCorrection = ewCorrection / n
    
    assumedLat = Angle.stringToAngle(assumedLat)
    assumedLat.decimal = assumedLat.hourDegree + (assumedLat.minuteDegree / 60)
    assumedLat.decimal = assumedLat.decimal + (nsCorrection / 60)
    left, right = str(assumedLat.decimal).split(".")
    right = "0." + right
    right = float(right)
    right = right * 60
    right = round(right, 1)
    
    result['presentLat'] = str(int(left)) + "d" + str(right)
    
    assumedLong = Angle.stringToAngle(assumedLong)
    assumedLong.decimal = assumedLong.hourDegree + (assumedLong.minuteDegree / 60)
    assumedLong.decimal = assumedLong.decimal + (ewCorrection / 60)
    left, right = str(assumedLong.decimal).split(".")
    right = "0." + right
    right = float(right)
    right = right * 60
    right = round(right, 1)
    
    result['presentLong'] = str(int(left)) + "d" + str(right)
    
    
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
        correctedAzmuth.decimal = correctedAzmuth.hourDegree + (correctedAzmuth.minuteDegree / 60)
        correctedDistance = float(correctedDistance)
        
        a = math.pow(((correctedDistance * math.cos(math.radians(correctedAzmuth.decimal))) - nsCorrection), 2)
        
        b = math.pow(((correctedDistance * math.sin(math.radians(correctedAzmuth.decimal))) - ewCorrection), 2)
        
        precision += math.sqrt(a + b)
    
    precision = (1.0 / n) * precision 
    left, right = str(precision).split(".")
    result['precision'] = left
    result['accuracy'] = 'NA'
    
    return result