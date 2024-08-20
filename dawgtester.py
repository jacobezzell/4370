"""
Jacob Ezzell
Aug 19th 2024
ICS 4370
Description: Unit testing for the dog output method.
"""

import unittest
from Mod_6_dogs import Dawg

dog_for_testing = Dawg("Bob", 10)

class poo_test(unittest.TestCase):
    def test_a_dog(self):
        self.assertIsInstance(dog_for_testing, Dawg)

    def test_dump(self):
        result = dog_for_testing.dump_list()
        self.assertIsInstance(result, list)

    def test_dump_accuracy(self):
        result = dog_for_testing.dump_list()
        self.assertEqual(result, ['Bob', 10, 11.5, 12.65])

def main():
    unittest.main()

if __name__ == "__main__":
    main()