'''
    Created on Ferbuary 18, 2018

    @author: William Hendrix
'''

import math

'''
    Adjust
        Input: a dictionary of values
        Output: an adjusted dictionary of values
'''      
def adjust(values = None):
    
    # ------ Validation ------    
    if values is None or not isinstance(values, dict):
        return {'error': 'values is not provided'}
    
    if (not('observation' in values)):
        return {'error': 'no observation provided'}
    
    if 'observation' in values:
        observation = values['observation']
        
        x, y = observation.split("d")
        if int(x) < 0 or int(x) > 89:
            return {'error': 'x is invalid'}
        
        y = y.lstrip("0")    
        if float(y) < 0.0 or not float(y) < 60:
            return {'error': 'y is invalid'}
        
        if int(x) == 0 and float(y) < 0.1:
            return {'error': 'observation is invalid'}
        
    if 'height' in values:
        height = values['height'] 
        
        try:
            height = float(height)
        except ValueError:
            {'error': 'height must be a float'}
        
        if (height < 0):
            return {'error': 'height must be greater than 0'}
        
    if 'pressure' in values:
        pressure = values['pressure']
        
        try:
            pressure = int(pressure)
        except ValueError:
            return {'error': 'pressure must be an int'}
        
        if pressure < 100 or pressure > 1100:
            return {'error': 'pressure is invalid'}
        
    if 'temperature' in values:
        temperature = values['temperature']
        
        try:
            temperature = int(temperature)
        except ValueError:
            return {'error': 'temperature must be an int'}
        
        if (temperature < 20 or temperature > 120):
            return {'error': 'temperature is invalid'}
        
    # ------ Initialization ------
    result = values
    
    if "height" in values:
        height = float(values['height'])
    else:
        height = 0
         
    if "pressure" in values:
        pressure = int(values['pressure'])
    else:
        pressure = 1010
         
    if "temperature" in values:
        temperature = int(values['temperature'])
    else: 
        temperature = 72
             
    if "horizon" in values:
        horizon = values['horizon']
    else:
        horizon = "natural"
    
    if horizon.lower() == "natural":
        dip = (-0.97 * math.sqrt(height)) / 60
    else:
        dip = 0
        
    # ------ Calculation ------
    observation = values['observation']
    x, y = observation.split("d")
    y = y.lstrip("0")
    observationDegree = int(x)
    observationMinute = float(y)
    
    observed = observationDegree + observationMinute / 60
    observedRadian = observed * math.pi / 180
    refraction = ((-0.00452 * pressure) / (273 + (temperature - 32) * 5 / 9)) / math.tan(observedRadian)
    
    adjusted = observed + dip + refraction
    degree = int(adjusted)
    minute = (adjusted - degree) * 60
    minute = round(minute, 1)
    
    if len(str(minute)) == 3:
        minute = "0" + str(minute)
    else:
        minute = str(minute)
    
    altitude = str(degree) + "d" + minute
    result['altitude'] = altitude
    
    return result






