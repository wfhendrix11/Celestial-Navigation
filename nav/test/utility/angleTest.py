import unittest

from nav.utility.angle import Angle

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
        