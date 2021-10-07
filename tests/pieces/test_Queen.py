import unittest

from ModularChess.controller.Board import Board
from ModularChess.pieces.Queen import Queen
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Position import Position
from tests.pieces.base_test_pieces import BaseTestPieces


class TestQueen(BaseTestPieces):
    __test__ = True

    def setUp(self) -> None:
        self.custom_setUp(Queen, Position("c4"), Position("e5"))

    def test_check_move(self):
        self.assertIsNotEmpty(self.piece1.check_move(Position("a6")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("a4")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("a2")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("c8")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("c1")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("g8")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("f1")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("h4")))
        self.assertIsEmpty(self.piece1.check_move(Position("d6")))
        self.assertIsEmpty(self.piece1.check_move(Position("g1")))

        self.assertIsNotEmpty(self.piece2.check_move(Position("a5")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("a1")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("b8")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("e8")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("e1")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("h8")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("h5")))
        self.assertIsNotEmpty(self.piece2.check_move(Position("h2")))
        self.assertIsEmpty(self.piece2.check_move(Position("h1")))
        self.assertIsEmpty(self.piece2.check_move(Position("c4")))

    def test_get_valid_moves(self):
        valid_moves = self.piece1.get_valid_moves()
        self.assertIn(BasicMovement(self.piece1, Position("a4")), valid_moves)
        self.assertIn(BasicMovement(self.piece1, Position("c8")), valid_moves)
        self.assertIn(BasicMovement(self.piece1, Position("a6")), valid_moves)
        self.assertNotIn(BasicMovement(self.piece1, Position("d1")), valid_moves)

        valid_moves = self.piece2.get_valid_moves()
        self.assertIn(BasicMovement(self.piece2, Position("e8")), valid_moves)
        self.assertIn(BasicMovement(self.piece2, Position("h2")), valid_moves)
        self.assertIn(BasicMovement(self.piece2, Position("h5")), valid_moves)
        self.assertNotIn(BasicMovement(self.piece2, Position("g1")), valid_moves)

    def test_capture(self):
        position = Position("c5")
        enemy_piece = Queen(self.board, self.other_player, position)
        self.board.add_piece(enemy_piece)

        self.assertIsNotEmpty(self.piece1.check_move(position))
        self.assertIsEmpty(self.piece1.check_move(Position("c6")))
        self.assertIn(BasicMovement(self.piece1, position), self.piece1.get_valid_moves())

        self.assertIsNotEmpty(self.piece2.check_move(position))
        self.assertIsEmpty(self.piece2.check_move(Position("b5")))
        self.assertIn(BasicMovement(self.piece2, position), self.piece2.get_valid_moves())

    def test_piece_in_path(self):
        position = Position("c5")
        ally_piece = Queen(self.board, self.main_player, position)
        self.board.add_piece(ally_piece)

        self.assertIsEmpty(self.piece1.check_move(position))
        self.assertIsEmpty(self.piece2.check_move(position))
        self.assertIsNotEmpty(self.piece2.check_move(Position("d5")))
        self.assertNotIn(BasicMovement(self.piece1, position), self.piece1.get_valid_moves())

    def test_multidimensional(self):
        self.board = Board((8, 8, 8))

        self.position1 = Position([3, 3, 3])
        self.piece1 = Queen(self.board, self.main_player, self.position1)
        self.board.add_piece(self.piece1)

        self.position2 = Position([3, 4, 3])
        self.piece2 = Queen(self.board, self.main_player, self.position2)
        self.board.add_piece(self.piece2)
        self.test_check_moves_same_as_get_valid_moves()


if __name__ == '__main__':
    unittest.main()
