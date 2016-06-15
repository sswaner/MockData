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

    def test_dict_contents(self):
        """Test that gen_first_name is returning a properly structured value.
        It must return a dict with 'given_name' and 'case'."""
        test_first_name = generator.gen_first_name()
        self.assertIn('given_name', generator.gen_first_name())
        self.assertIn('case', generator.gen_first_name())
        # "seed" key is not required.

class TestLastName(unittest.TestCase):
    """Test gen_last_name funtion:  Must return a dict with random values
        for the given_name key and a case key."""

    def test_not_none(self):
        """Test gen_last_name.  Must return a value."""
        self.assertIsNotNone(generator.gen_last_name(), 
                             "gen_last_name() didn't return a value.")

    def test_dict_type(self):
        """Check that return value is a dict."""
        self.assertIs(type(generator.gen_last_name()), dict,
                      "gen_last_name return type was not dict.")

    def test_random(self):
        """Generate 4 first names and test that they are all differnt."""
        test1 = generator.gen_last_name()
        test2 = generator.gen_last_name()
        test3 = generator.gen_last_name()
        test4 = generator.gen_last_name()


        self.assertFalse(test1 == test2 == test3 == test4,
                         "gen_last_name is not creating random names.")

    def test_dict_contents(self):
        """Test that gen_last_name is returning a properly structured value.
        It must return a dict with 'given_name' and 'case'."""
        test_first_name = generator.gen_last_name()
        self.assertIn('last_name', generator.gen_last_name())
        self.assertIn('case', generator.gen_last_name())

class TestCreditCard(unittest.TestCase):
    """Test the gen_credit_card function in generator.py."""    

    def test_not_none(self):
        """Test gen_credit_card_number.  Must return a value."""
        self.assertIsNotNone(generator.gen_credit_card_number(), 
                             "gen_credit_card_number didn't return a value.")
    def test_numeric(self):
        self.assertIs(int(generator.gen_credit_card_number()), int, 
                      "gen_credit_card_number did not return a numeric value")

if __name__ == '__main__':
    unittest.main(verbosity=3)
