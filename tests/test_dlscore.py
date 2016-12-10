import unittest

from numpy import asarray

from rnglib import dlscore

ai = lambda x: asarray(x, dtype='i')


class TestDlscore(unittest.TestCase):
    def test_align(self):
        pattern = ai([1, 2, ])
        sequence = ai([0, 0, 0, 1, 2, 3, 0, 0, 0])
        expected = ai([2, 2, 2, 1, 0, 1, 2, 2, 2])
        returned = dlscore.align(pattern, sequence, 1, 1, 1, 1)
        assert (expected == returned).all()

    def test_score(self):
        pattern = ai([1, 2, ])
        sequence = ai([0, 0, 0, 1, 2, 3, 0, 0, 0])
        expected_alignment = ai([2, 2, 2, 1, 0, 1, 2, 2, 2])
        expected_score = sum(1. / (expected_alignment + 1)) / len(sequence)
        returned_score = dlscore.score(pattern, sequence, 1, 1, 1, 1)
        self.assertAlmostEqual(returned_score, expected_score)

    def test_iter_scores(self):
        self.fail()

    def test_array_scores(self):
        self.fail()
