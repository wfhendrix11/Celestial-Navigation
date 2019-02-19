import math

# Defaults
height = 0
pressure = 1010
temperature = 72
horizon = "natural"
dip = 0

# Adjust       
def adjust(values = None):
    
    result = values
    
    if "height" in values:
        height = float(values['height'])
         
    if "pressure" in values:
        pressure = int(values['pressure'])
         
    if "temperature" in values:
        temperature = int(values['temperature'])
             
    if "horizon" in values:
        horizon = values['horizon']
    
    if horizon.lower() == "natural":
        dip = (-0.97 * math.sqrt(height)) / 60
        
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






