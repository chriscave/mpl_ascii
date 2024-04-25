import unittest

import numpy as np
from numpy import array_equal

from mpl_ascii.overlay import overlay

class TestOverlay(unittest.TestCase):

    def test_basic_overlap(self):
        back = np.array(
            [
                ["x", "x", "x"],
                ["x", "x", "x"],
                ["x", "x", "x"],
            ]
        )
        fore = np.array(
            [
                ["y", "y"],
                ["y", "y"],
            ]
        )
        actual = overlay(back, fore, 1,1)
        expected = np.array(
            [
                ["x", "x", "x"],
                ["x", "y", "y"],
                ["x", "y", "y"],
            ]
        )

        self.assertTrue(array_equal(actual, expected))

    def test_negative_start_conditions(self):
        back = np.array([["1"]*5]*5)
        fore = np.array(
            [
                ["y", "x"],
                ["x", "y"],
            ]
        )
        actual = overlay(back, fore, -1, -1)
        expected = np.array(
            [
                ["y", "x", " ", " ", " ", " "],
                ["x", "y", "1", "1", "1", "1"],
                [" ", "1", "1", "1", "1", "1"],
                [" ", "1", "1", "1", "1", "1"],
                [" ", "1", "1", "1", "1", "1"],
                [" ", "1", "1", "1", "1", "1"],
            ]
        )
        self.assertTrue(array_equal(actual, expected))

    def test_foreground_bigger_than_background(self):
        background = np.array([
            ["2", "2", "2"],
            ["2", "2", "2"],
            ["2", "2", "2"]
        ])
        foreground = np.array([
            ["A", "B", "C", "D", "E"],
            ["F", "G", "H", "I", "J"],
            ["K", "L", "M", "N", "O"],
            ["P", "Q", "R", "S", "T"],
            ["U", "V", "W", "X", "Y"]
        ])
        expected = foreground
        actual = overlay(background, foreground, 0,0)
        self.assertTrue(array_equal(actual, expected))

    def test_foreground_whitespace(self):
        background = np.array([
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"],
            ["9", "A", "B", "C"],
            ["D", "E", "F", "G"]
        ])
        foreground = np.array([
            ["X", " "],
            ["Y", "Z"]
        ])
        expected = np.array([
            ["X", "2", "3", "4"],
            ["Y", "Z", "7", "8"],
            ["9", "A", "B", "C"],
            ["D", "E", "F", "G"]
        ])
        actual = overlay(background, foreground, 0,0)

        self.assertTrue(array_equal(actual, expected))

    def test_all_whitespace_foreground(self):
        background = np.array([
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"],
            ["9", "A", "B", "C"],
            ["D", "E", "F", "G"]
        ])

        foreground = np.array(
            [
                [" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "],
            ]
        )
        expected = np.array(
            [
                ["1", "2", "3", "4", " "],
                ["5", "6", "7", "8", " "],
                ["9", "A", "B", "C", " "],
                ["D", "E", "F", "G", " "],
                [" ", " ", " ", " ", " "]
            ]
        )
        actual = overlay(background, foreground, 2, 2)
        self.assertTrue(array_equal(actual, expected))

    def test_foreground_outside_backgroud(self):
        back = np.array(
            [
                ["x", "x", "x"],
                ["x", "x", "x"],
                ["x", "x", "x"],
            ]
        )
        fore = np.array(
            [
                ["y", "y"],
                ["y", "y"],
            ]
        )
        actual = overlay(back, fore, -3,-3)
        expected = np.array(
            [
                ["y", "y", " ", " ", " ", " "],
                ["y", "y", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " "],
                [" ", " ", " ", "x", "x", "x"],
                [" ", " ", " ", "x", "x", "x"],
                [" ", " ", " ", "x", "x", "x"],
            ]
        )

        self.assertTrue(array_equal(actual, expected))

    def test_empty_background(self):
        background = np.array([]).reshape(0, 0)  # An empty (0x0) array
        foreground = np.array([
            ["Q", "Q"],
            ["Q", "Q"]
        ])
        actual = overlay(background, foreground, 0,0)

        expected = np.array([
            ["Q", "Q"],
            ["Q", "Q"]
        ])
        self.assertTrue(array_equal(actual, expected))


