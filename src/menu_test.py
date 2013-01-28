# Unit tests for menu class
import unittest, overlay

class MenuTest(unittest.TestCase):
    def setUp(self):
        self.destination = 0 # Placeholder for pygame surface.
        self.testMenu = overlay.MenuBox( self.destination, ["Selection 1", "Selection 2", "Selection 3"], [0, 0, 0])
    
    def test_emptyItemsList(self):
       self.assertRaises(IndexError, overlay.MenuBox, self.destination, [], [])
        
    def test_inconsistentArguments(self):
        self.assertRaises(IndexError, overlay.MenuBox, self.destination, [1, 2, 3], [1, 2])
        
    def test_updateCursorPosition(self):
        self.testMenu.selected = 0
        self.testMenu.updateCursorPosition("up")
        self.assertTrue(self.testMenu.selected == 1)