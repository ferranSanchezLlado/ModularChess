import unittest

import numpy as np

from ModularChess.utils.Position import Position


class TestPosition(unittest.TestCase):

    def test_create_with_chess_notation(self):
        pos1 = "a1"
        test1 = Position(pos1)
        truth1 = Position([0, 0])

        pos2 = "f3"
        test2 = Position(pos2)
        truth2 = Position([2, 5])

        pos3 = "h8"
        test3 = Position(pos3)
        truth3 = Position([7, 7])

        for test, truth, pos in zip([test1, test2, test3], [truth1, truth2, truth3], [pos1, pos2, pos3]):
            self.assertListEqual(truth.tolist(), test.tolist())
            self.assertTrue(np.array_equal(truth, test))

            # Checks str representation is correct
            self.assertEqual(pos, str(test))
            self.assertEqual(pos, str(truth))

    def test_create_lineal_path(self):
        orig = Position([1, 2, 3])
        dest1 = Position([0, 0])

        # Different dimensions
        with self.assertRaises(Exception):
            list(orig.create_lineal_path(destination=dest1))

        dest2 = Position([0, 0, 0])
        # Not lineal path
        with self.assertRaises(Exception):
            list(orig.create_lineal_path(destination=dest2))

        # 1 axis change
        dest3 = Position([3, 2, 3])
        true_path_3 = [Position([2, 2, 3]), Position([3, 2, 3])]
        path_3 = list(orig.create_lineal_path(destination=dest3))

        # 3 axis change
        dest4 = Position([3, 0, 1])
        true_path_4 = [Position([2, 1, 2]), Position([3, 0, 1])]
        path_4 = list(orig.create_lineal_path(destination=dest4))

        for path, true_path in zip([path_3, path_4], [true_path_3, true_path_4]):
            for pos, truth in zip(path, true_path):
                self.assertListEqual(truth.tolist(), pos.tolist())
                self.assertTrue(np.array_equal(truth, pos))

    def test_copy_and_replace(self):
        test1 = Position([1, 2])
        copy1 = test1.copy_and_replace(0, 1)  # Changes to same value
        self.assertIsNot(test1, copy1)
        self.assertTrue(np.array_equal(test1, copy1))

        test2 = Position([1, 2, 3, 4])
        copy2 = test2.copy_and_replace(0, 2)
        self.assertIsNot(test2, copy2)
        self.assertFalse(np.array_equal(test2, copy2))
        self.assertEqual(2, copy2[0])

        test3 = Position([6, 6, 6])
        copy3 = test3.copy_and_replace(1, 10)
        self.assertIsNot(test3, copy3)
        self.assertFalse(np.array_equal(test3, copy3))
        self.assertEqual(10, copy3[1])

    def test_not_int(self):
        self.assertRaises(Exception, Position, coord=["a", "b", "c"])
        self.assertRaises(Exception, Position, coord=[1.1, 1.2, 1.3])
        self.assertRaises(Exception, Position, coord=["a", 1, 2])

    def test_str(self):
        pos = Position([1, 2, 3])
        self.assertEqual("(1, 2, 3)", str(pos))

        pos = Position("a2")
        self.assertEqual("a2", str(pos))


if __name__ == '__main__':
    unittest.main()
