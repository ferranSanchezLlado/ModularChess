import unittest

from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.movements.BasicMovement import BasicMovement
from ModularChess.movements.Movement import MovementData
from ModularChess.pieces.Empty import Empty
from ModularChess.utils.Position import Position


class TestBasicMovement(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board((8, 8))
        self.player1 = Player("test")
        self.piece_position1 = Position([self.board.size // 2] * self.board.dimensions)
        self.piece1 = Empty(self.board, self.player1, self.piece_position1)

        self.player2 = Player("test2")
        self.piece_position2 = Position([self.board.size - 1] * self.board.dimensions)
        self.piece2 = Empty(self.board, self.player2, self.piece_position2)

        self.board.add_piece(self.piece1)
        self.board.add_piece(self.piece2)

    def test_move_to_empty(self):
        position = Position([0] * self.board.dimensions)
        move = BasicMovement(self.piece1, position)

        self.assertEqual(1, len(move.movements))
        self.assertTupleEqual((MovementData(self.piece1, self.piece_position1, position),), move.movements)
        self.assertEqual(move, self.piece1.check_piece_valid_move(position)[0])
        self.assertTrue(move.check_valid_move())

    def test_move_to_capture(self):
        move = BasicMovement(self.piece1, self.piece_position2)

        self.assertEqual(2, len(move.movements))
        self.assertTupleEqual(((MovementData(self.piece2, self.piece_position2, None),
                                MovementData(self.piece1, self.piece_position1, self.piece_position2))), move.movements)
        self.assertEqual(move, self.piece1.check_piece_valid_move(self.piece_position2)[0])
        self.assertTrue(move.check_valid_move())


if __name__ == '__main__':
    unittest.main()
