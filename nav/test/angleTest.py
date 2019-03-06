import unittest
from nav.angle import Angle

class AngleTest(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test100_010ShouldReturnStringConvertedToAngle(self):
        # Arrange
        # Act
        angle = Angle.stringToAngle("164d54.5") 
        
        # Assert       
        self.assertEqual(angle.hourDegree, 164)
        self.assertEqual(angle.minuteDegree, 54.5)
        self.assertAlmostEqual(angle.decimal, 0.458, places=3)
    
    def test200_010ShouldReturnDecimalConvertedToAngle(self):
        # Arrange
        # Act
        angle = Angle.decimalToAngle(16.180079)
        
        # Assert
        self.assertEqual(angle.hourDegree, 64)
        self.assertEqual(angle.minuteDegree, 49.7)
        
    def test300_010ShouldReturnSumOfAngles(self):
        # Arrange
        # Act
        angle1 = Angle.stringToAngle("100d4.8")
        angle2 = Angle.stringToAngle("-1d0.0")
        
        # Assert
        result = Angle.add(angle1, angle2)
        self.assertEqual(result.str, "99d4.8")
    
    def test400_010ShouldReturnProductOfAngles(self):
        # Arrange
        # Act
        angle = Angle.stringToAngle("0d59.0")
        result = Angle.multiply(angle, 3)
        
        # Assert
        self.assertEqual(result.str, "2d56.9")
        