"""Test cases for generator.py"""
import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from MockData import generator

class TestFirstName(unittest.TestCase):
    """Test gen_first_name funtion:  Must return a dict with random values
        for the given_name key and a case key."""

    def test_not_none(self):
        """Test gen_first_name.  Must return a value."""
        self.assertIsNotNone(generator.gen_first_name(), "gen_first_name() didn't return a value.")

    def test_dict_type(self):
        """Check that return value is a dict."""
        self.assertIs(type(generator.gen_first_name()), dict)

    def test_random(self):
        """Generate 4 first names and test that they are all differnt."""
        test1 = generator.gen_first_name()
        test2 = generator.gen_first_name()
        test3 = generator.gen_first_name()
        test4 = generator.gen_first_name()


        self.assertFalse(test1 == test2 == test3 == test4,
                         "gen_first_name is not creating random names.")

        #test the required elements of the dict are present
    def test_dict_contents(self):
        """Test that gen_first_name is returning a properly structured value.
        It must return a dict with 'given_name' and 'case'."""
        test_first_name = generator.gen_first_name()
        self.assertIn('given_name', test_first_name)
        self.assertIn('case', test_first_name)

if __name__ == '__main__':
    unittest.main(verbosity=3)
