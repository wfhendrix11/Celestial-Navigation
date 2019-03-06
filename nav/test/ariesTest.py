'''
Created on March 1, 2018

@author: William Hendrix
'''

import unittest
from nav.aries import Aries

class AriesTest(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test100_ShouldReturnGreenwichHourAngle(self):
        angle = Aries.getGreenwichHourAngle(2016, 1, 17, 3, 15, 42)
        self.assertEqual(angle.str, "164d54.5")