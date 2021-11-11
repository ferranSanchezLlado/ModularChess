import unittest

from ModularChess.controller.Board import Board
from ModularChess.movements.BasicMovement import BasicMovement
from ModularChess.pieces.Knight import Knight
from ModularChess.utils.Position import Position
from pieces.base_test_pieces import BaseTestPieces


class TestKnight(BaseTestPieces):
    __test__ = True

    def setUp(self) -> None:
        self.custom_setUp(Knight, Position("d4"), Position("e4"))

    def test_check_move(self):
        self.assertIsNotEmpty(self.piece1.check_piece_valid_move(Position("b3")))
        self.assertIsNotEmpty(self.piece1.check_piece_valid_move(Position("c6")))
        self.assertIsNotEmpty(self.piece1.check_piece_valid_move(Position("e2")))
        self.assertIsNotEmpty(self.piece1.check_piece_valid_move(Position("f5")))
        self.assertIsEmpty(self.piece1.check_piece_valid_move(Position("b6")))
        self.assertIsEmpty(self.piece1.check_piece_valid_move(Position("d1")))

        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(Position("c5")))
        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(Position("d2")))
        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(Position("f6")))
        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(Position("g3")))
        self.assertIsEmpty(self.piece2.check_piece_valid_move(Position("h1")))
        self.assertIsEmpty(self.piece2.check_piece_valid_move(Position("c7")))

    def test_get_valid_moves(self):
        valid_moves = self.piece1.get_piece_valid_moves()
        self.assertIn(BasicMovement(self.piece1, Position("b3")), valid_moves)
        self.assertIn(BasicMovement(self.piece1, Position("c6")), valid_moves)
        self.assertIn(BasicMovement(self.piece1, Position("e2")), valid_moves)
        self.assertIn(BasicMovement(self.piece1, Position("f5")), valid_moves)
        self.assertNotIn(BasicMovement(self.piece1, Position("d8")), valid_moves)

        valid_moves = self.piece2.get_piece_valid_moves()
        self.assertIn(BasicMovement(self.piece2, Position("c5")), valid_moves)
        self.assertIn(BasicMovement(self.piece2, Position("d2")), valid_moves)
        self.assertIn(BasicMovement(self.piece2, Position("f6")), valid_moves)
        self.assertIn(BasicMovement(self.piece2, Position("g3")), valid_moves)
        self.assertNotIn(BasicMovement(self.piece2, Position("e2")), valid_moves)

    def test_capture(self):
        position = Position("c5")
        enemy_piece = Knight(self.board, self.other_player, position)
        self.board.add_piece(enemy_piece)

        self.assertIsNotEmpty(self.piece2.check_piece_valid_move(position))
        self.assertIn(BasicMovement(self.piece2, position), self.piece2.get_piece_valid_moves())

    def test_multidimensional(self):
        self.board = Board((8, 8, 8))

        self.position1 = Position([3, 3, 3])
        self.piece1 = Knight(self.board, self.main_player, self.position1)
        self.board.add_piece(self.piece1)

        self.position2 = Position([3, 4, 3])
        self.piece2 = Knight(self.board, self.main_player, self.position2)
        self.board.add_piece(self.piece2)
        self.test_check_moves_same_as_get_valid_moves()


if __name__ == '__main__':
    unittest.main()
