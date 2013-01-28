# Test cases for Entity class

import unittest, Entity

class EntityTest(unittest.TestCase):
    def setUp(self):
        self.e = entity.Entity("Name", 0, 0)
    def test_name(self):
        self.assertEqual(self.e.name, "Name")
    def test_location(self):
        self.assertEqual(self.e.mapLocation, (0,0))
