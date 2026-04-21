# Long Vy
# IN450 - Unit 4
# 04/21/2026


"""
test_modules.py
Unit 4 Assignment - Unit tests for the three modules.
Run with:  python -m unittest test_modules.py -v
"""

import io
import unittest
from unittest.mock import patch

from IN450_LongVy_Unit4_Modules  import example1, example2, example3


class TestExample1(unittest.TestCase):
    """Tests for example1 — finds the min value in first n elements."""

    def test_returns_smallest_value_in_range(self):
        result = example1([7, 3, 9, 1, 12], 5)
        self.assertEqual(result, 1)

    def test_returns_100_when_all_values_exceed_100(self):
        result = example1([150, 200, 175], 3)
        self.assertEqual(result, 100)


class TestExample2(unittest.TestCase):
    """Tests for example2 — prints the first 100 elements of the array."""

    def test_prints_one_hundred_lines(self):
        test_data = list(range(100))
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            example2(test_data)
            output_lines = fake_out.getvalue().strip().split("\n")
        self.assertEqual(len(output_lines), 100)

    def test_prints_correct_values_in_order(self):
        test_data = list(range(100))
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            example2(test_data)
            output_lines = fake_out.getvalue().strip().split("\n")
        self.assertEqual(output_lines[0], "0")
        self.assertEqual(output_lines[99], "99")


class TestExample3(unittest.TestCase):
    """Tests for example3 — searches array for values 10 and 5."""

    def test_prints_found_message_when_value_present(self):
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            example3([1, 2, 10, 4, 7])
            output = fake_out.getvalue()
        self.assertIn("found in int array", output)
        self.assertNotIn("None of the search values were found.", output)

    def test_prints_not_found_message_when_values_absent(self):
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            example3([1, 2, 3, 4, 7])
            output = fake_out.getvalue()
        self.assertIn("None of the search values were found.", output)


if __name__ == "__main__":
    unittest.main()