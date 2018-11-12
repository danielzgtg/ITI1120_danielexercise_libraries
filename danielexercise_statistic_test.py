# Test the histogram, and sorted_dict_pairs functions in danielexercise_statistic
# Type: Unit Tests

import unittest
from danielexercise_statistic import histogram, sorted_dict_pairs


class TestMatrixMethods(unittest.TestCase):
    def test_histogram_handout1(self):
        text = "les saucisses et saucissons secs sont dans le saloir"
        hist_expected = {
            ' ': 8,
            'a': 4,
            'e': 5,
            'c': 3,
            'd': 1,
            'i': 3,
            'l': 3,
            'n': 3,
            'o': 3,
            'r': 1,
            's': 14,
            't': 2,
            'u': 2,
        }
        hist_actual = histogram(text)
        self.assertEqual(hist_expected, hist_actual)

        sorted_expected = [
            (' ', 8),
            ('a', 4),
            ('c', 3),
            ('d', 1),
            ('e', 5),
            ('i', 3),
            ('l', 3),
            ('n', 3),
            ('o', 3),
            ('r', 1),
            ('s', 14),
            ('t', 2),
            ('u', 2),
        ]
        sorted_actual = sorted_dict_pairs(hist_actual)
        self.assertEqual(sorted_expected, sorted_actual)

    def test_histogram_handout2(self):
        given = (1, 2, -3, 3, 4, -3, 3, 3)
        hist_expected = {
            -3: 2,
            1: 1,
            2: 1,
            3: 3,
            4: 1,
        }
        hist_actual = histogram(given)
        self.assertEqual(hist_expected, hist_actual)


if __name__ == "__main__":
    unittest.main()
