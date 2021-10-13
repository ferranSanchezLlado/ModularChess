import unittest
from typing import List

import numpy as np

from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.pieces.Empty import Empty
from ModularChess.utils.Movement import Movement, MovementData
from ModularChess.utils.Position import Position


class TestMovement(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board()
        self.player = Player("test")
        self.piece_position = Position([self.board.size // 2] * self.board.dimensions)
        self.piece_destination = Position([0] * self.board.dimensions)
        self.piece = Empty(self.board, self.player, self.piece_position)

        class TemporalMovement(Movement):
            def __init__(self, moves: List[MovementData]):
                super().__init__(moves)

        self.move = TemporalMovement([MovementData(self.piece, None, self.piece_position),
                                      MovementData(self.piece, self.piece_position, self.piece_destination),
                                      MovementData(self.piece, self.piece_destination, None)])

    def test_move(self):
        self.move.move()

        self.assertTrue(np.array_equal(self.piece_destination, self.piece.position))
        self.assertEqual(1, self.piece.n_moves)

        self.setUp()
        self.move.movements.pop()
        self.move.move()

        self.assertTrue(np.array_equal(self.piece_destination, self.piece.position))
        self.assertEqual(1, self.piece.n_moves)

    def test_inverse(self):
        self.move.movements.pop()

        inverse = self.move.inverse()
        self.assertListEqual([MovementData(self.piece, self.piece_destination, self.piece_position),
                              MovementData(self.piece, self.piece_position, None)], inverse.movements)

        self.move.move()
        inverse.move()

        self.assertTrue(np.array_equal(self.piece_position, self.piece.position))
        self.assertEqual(0, self.piece.n_moves)


if __name__ == '__main__':
    unittest.main()
