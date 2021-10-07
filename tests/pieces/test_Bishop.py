import unittest

from ModularChess.controller.Board import Board
from ModularChess.pieces.Bishop import Bishop
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Position import Position
from tests.pieces.base_test_pieces import BaseTestPieces


class TestBishop(BaseTestPieces):
    __test__ = True

    def setUp(self) -> None:
        self.custom_setUp(Bishop, Position("d4"), Position("e4"))

    def test_check_move(self):
        self.assertIsNotEmpty(self.piece1.check_move(Position("a7")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("a1")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("h8")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("g1")))
        self.assertIsEmpty(self.piece1.check_move(Position("a8")))
        self.assertIsEmpty(self.piece1.check_move(Position("e4")))

        self.assertIsNotEmpty(self.piece2.check_move(Position("f5")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("f3")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("d5")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("d3")))
        self.assertIsEmpty(self.piece2.check_move(Position("e5")))
        self.assertIsEmpty(self.piece2.check_move(Position("e8")))

    def test_get_valid_moves(self):
        valid_moves = self.piece1.get_valid_moves()
        self.assertIn(BasicMovement(self.piece1, Position("b2")), valid_moves)
        self.assertIn(BasicMovement(self.piece1, Position("c5")), valid_moves)
        self.assertIn(BasicMovement(self.piece1, Position("e3")), valid_moves)
        self.assertNotIn(BasicMovement(self.piece1, Position("d8")), valid_moves)

        valid_moves = self.piece2.get_valid_moves()
        self.assertIn(BasicMovement(self.piece2, Position("f3")), valid_moves)
        self.assertIn(BasicMovement(self.piece2, Position("c6")), valid_moves)
        self.assertIn(BasicMovement(self.piece2, Position("g6")), valid_moves)
        self.assertNotIn(BasicMovement(self.piece2, Position("e2")), valid_moves)

    def test_capture(self):
        position = Position("b7")
        enemy_piece = Bishop(self.board, self.other_player, position)
        self.board.add_piece(enemy_piece)

        self.assertIsNotEmpty(self.piece2.check_move(position))
        self.assertIsEmpty(self.piece2.check_move(Position("a8")))
        self.assertIn(BasicMovement(self.piece2, position), self.piece2.get_valid_moves())

    def test_piece_in_path(self):
        position = Position("b6")
        ally_piece = Bishop(self.board, self.main_player, position)
        self.board.add_piece(ally_piece)

        self.assertIsEmpty(self.piece1.check_move(position))
        self.assertIsNotEmpty(self.piece1.check_move(Position("c5")))
        self.assertNotIn(BasicMovement(self.piece1, position), self.piece1.get_valid_moves())

    def test_multidimensional(self):
        self.board = Board((8, 8, 8))

        self.position1 = Position([3, 3, 3])
        self.piece1 = Bishop(self.board, self.main_player, self.position1)
        self.board.add_piece(self.piece1)

        self.position2 = Position([3, 4, 3])
        self.piece2 = Bishop(self.board, self.main_player, self.position2)
        self.board.add_piece(self.piece2)
        self.test_check_moves_same_as_get_valid_moves()


if __name__ == '__main__':
    unittest.main()
