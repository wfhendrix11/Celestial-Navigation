'''
Created on March 1, 2018

@author: William Hendrix
'''

import math
import re

class Angle:
    
    '''
    Constructor
        :param none
        :return none
    '''   
    def __init__(self, hourDegree, minuteDegree):
        if minuteDegree < 0:
            raise ValueError("minute degree must be positive!")
        
        self.hourDegree = int(hourDegree)
        self.minuteDegree = float(minuteDegree)
        self.str = str(hourDegree) + "d" + str(minuteDegree)
        
        if '-' in str(hourDegree):
            self.isNegative = True
            self.decimal = (self.hourDegree - (self.minuteDegree / 60.0)) / 360.0
        else:
            self.decimal = (self.hourDegree + (self.minuteDegree / 60.0)) / 360.0 
    
    '''
    add
        :param two angles
        :return sum of the angles
    ''' 
    @classmethod          
    def add(cls, angle1 = None, angle2 = None):
        result = angle1.decimal + angle2.decimal
        return Angle.decimalToAngle(result)
    
    '''
    multiply
        :param angle and a number
        :return product of the angle and number
    ''' 
    @classmethod 
    def multiply(cls, angle = None, number = None):      
        result = angle.decimal * number
        return Angle.decimalToAngle(result)
    
    '''
    stringToAngle
        :param string
        :return sum of the angles
    '''
    @classmethod
    def stringToAngle(cls, string):
        hourDegree = 0
        minuteDegree = 0
        
        angleString = re.match('^[-]?[0-9]+d[0-9]+.[0-9]+$', string)
        
        if angleString:
            observation = angleString.group()
            
            x, y = observation.split("d")
            if int(x) < -360 or int(x) > 360:
                return {'error': 'observation degree is invalid'}
        
            y = y.lstrip("0")
            if float(y) < 0.0 or not float(y) < 60:
                return {'error': 'angle is invalid'}
            
            if (int(x) == 360 or int(x) == -360) and float(y) > 0.0:
                return {'error': 'observation degree is invalid'}
            
            hourDegree = x
            minuteDegree = y
            
            return Angle(hourDegree, minuteDegree)
    
    '''
    stringToAngle
        :param decimal
        :return sum of the angles
    '''
    @classmethod       
    def decimalToAngle(cls, decimal = None):
        
        negative = decimal < 0
        (left, right) = str(decimal).split(".")
        right = "0." + right
        hours = int(math.floor(float(right) * 360.0))
        
        minute = round(float(right), 5) * 360.0000
        (left, right) = str(minute).split(".")
        right = "0." + right
        right = round(float(right), 7) * 60.00000000
        minuteDec = round(right, 1)
        
        if negative:
            hours = -hours
            
        return Angle(hours, minuteDec)
    
    
    
    
    
    
    
    