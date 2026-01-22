"""
Unit test for helper functions in position.py
"""
import unittest

from position import *

class Tests(unittest.TestCase):
    def test_position(self):
        a = Position(2, 3, 5)
        b = Position(4, 1, 5)
        self.assertEqual(a.length, 1)
        self.assertEqual(b.length, 2)
        self.assertEqual(overlap(a, b), False)
        self.assertEqual(get_distance(a, b), 1)
        a += 1
        self.assertEqual(a,bounds, (3, 4))
        self.assertEqual(overlap(a, b), True)


unittest.main()
