# Test the transpose, sum_matrices, and multiply_matrices functions in danielexercise_matrix
# Type: Unit Tests

import unittest
from danielexercise_matrix import transpose, sum_matrices, multiply_matrices


class TestMatrixMethods(unittest.TestCase):
    def test_transpose_handout1(self):
        given = [
            [1, 2, 3],
            [4, 5, 6],
        ]
        expected = [
            [1, 4],
            [2, 5],
            [3, 6],
        ]
        actual = transpose(given)
        self.assertEqual(expected, actual)

    def test_sum_handout1(self):
        given_1 = [
            [1, 2],
            [3, 4],
        ]
        given_2 = [
            [1, 1],
            [1, 1],
        ]
        expected = [
            [2, 3],
            [4, 5],
        ]
        actual = sum_matrices(given_1, given_2)
        self.assertEqual(expected, actual)

    def test_multiply_handout1(self):
        given1 = [
            [1, 2, 3],
            [4, 5, 6],
        ]
        given2 = [
            [1, 2],
            [3, 4],
            [5, 6],
        ]
        expected = [
            [22, 28],
            [49, 64],
        ]
        actual = multiply_matrices(given1, given2)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
