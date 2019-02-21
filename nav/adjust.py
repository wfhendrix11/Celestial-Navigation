import math

# Adjust       
def adjust(values = None):
    
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






