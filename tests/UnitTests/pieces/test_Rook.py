import unittest

from ModularChess.controller.Board import Board
from ModularChess.movements.BasicMovement import BasicMovement
from ModularChess.pieces.Rook import Rook
from ModularChess.utils.Position import Position
from pieces.base_test_pieces import BaseTestPieces


class TestQueen(BaseTestPieces):
    __test__ = True

    def setUp(self) -> None:
        self.custom_setUp(Rook, Position("d4"), Position("e5"))

    def test_check_move(self):
        self.assertIsNotEmpty(self.piece1.check_piece_valid_move(Position("a4")))
        self.assertIsNotEmpty(self.piece1.check_piece_valid_move(Position("d1")))
        self.assertIsNotEmpty(self.piece1.check_piece_valid_move(Position("d8")))
        self.assertIsNotEmpty(self.piece1.check_piece_valid_move(Position("h4")))
        self.assertIsEmpty(self.piece1.check_piece_valid_move(Position("a1")))
        self.assertIsEmpty(self.piece1.check_piece_valid_move(Position("e5")))

        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(Position("a5")))
        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(Position("e1")))
        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(Position("e8")))
        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(Position("h5")))
        self.assertIsEmpty(self.piece2.check_piece_valid_move(Position("h8")))
        self.assertIsEmpty(self.piece2.check_piece_valid_move(Position("a6")))

    def test_get_valid_moves(self):
        valid_moves = self.piece1.get_piece_valid_moves()
        self.assertIn(BasicMovement(self.piece1, Position("b4")), valid_moves)
        self.assertIn(BasicMovement(self.piece1, Position("d7")), valid_moves)
        self.assertIn(BasicMovement(self.piece1, Position("e4")), valid_moves)
        self.assertNotIn(BasicMovement(self.piece1, Position("c3")), valid_moves)

        valid_moves = self.piece2.get_piece_valid_moves()
        self.assertIn(BasicMovement(self.piece2, Position("e4")), valid_moves)
        self.assertIn(BasicMovement(self.piece2, Position("g5")), valid_moves)
        self.assertIn(BasicMovement(self.piece2, Position("e8")), valid_moves)
        self.assertNotIn(BasicMovement(self.piece2, Position("d3")), valid_moves)

    def test_capture(self):
        position = Position("d6")
        enemy_piece = Rook(self.board, self.other_player, position)
        self.board.add_piece(enemy_piece)

        self.assertIsNotEmpty(self.piece1.check_piece_valid_move(position))
        self.assertIsEmpty(self.piece1.check_piece_valid_move(Position("d7")))
        self.assertIn(BasicMovement(self.piece1, position), self.piece1.get_piece_valid_moves())

    def test_piece_in_path(self):
        position = Position("c5")
        ally_piece = Rook(self.board, self.main_player, position)
        self.board.add_piece(ally_piece)

        self.assertIsEmpty(self.piece2.check_piece_valid_move(position))
        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(Position("d5")))
        self.assertNotIn(BasicMovement(self.piece1, position), self.piece1.get_piece_valid_moves())

    def test_multidimensional(self):
        self.board = Board((8, 8, 8))

        self.position1 = Position([3, 3, 3])
        self.piece1 = Rook(self.board, self.main_player, self.position1)
        self.board.add_piece(self.piece1)

        self.position2 = Position([3, 4, 3])
        self.piece2 = Rook(self.board, self.main_player, self.position2)
        self.board.add_piece(self.piece2)
        self.test_check_moves_same_as_get_valid_moves()


if __name__ == '__main__':
    unittest.main()
