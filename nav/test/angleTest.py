import unittest
from nav.angle import Angle

class AngleTest(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test100_010ShouldReturnStringConvertedToAngle(self):
        angle = Angle.stringToAngle("164d54.5")        
        self.assertEqual(angle.hourDegree, 164)
        self.assertEqual(angle.minuteDegree, 54.5)
        self.assertAlmostEqual(angle.decimal, 0.458, places=3)
    
    def test200_010ShouldReturnDecimalConvertedToAngle(self):
        angle = Angle.decimalToAngle(16.180079)
        
        self.assertEqual(angle.hour_degree, 64)
        self.assertEqual(angle.minute_degree, 49.7)
        