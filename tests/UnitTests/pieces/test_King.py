import unittest

from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.movements.BasicMovement import BasicMovement
from ModularChess.movements.Castling import Castling
from ModularChess.pieces.Empty import Empty
from ModularChess.pieces.King import King
from ModularChess.pieces.Rook import Rook
from ModularChess.utils.Position import Position
from pieces.base_test_pieces import BaseTestPieces


class TestKing(BaseTestPieces):
    __test__ = True

    def setUp(self) -> None:
        self.board = Board()
        self.main_player = Player("White")
        self.other_player = Player("Black")

        players = [self.main_player, self.other_player]
        Player.join_allies([self.main_player], players)
        Player.join_allies([self.other_player], players)

        self.king_position = Position("e1")
        self.king = King(self.board, self.main_player, self.king_position)
        self.board.add_piece(self.king)

        self.rook_position1 = Position("a1")
        self.rook1 = Rook(self.board, self.main_player, self.rook_position1)
        self.board.add_piece(self.rook1)

        self.rook_position2 = Position("h1")
        self.rook2 = Rook(self.board, self.main_player, self.rook_position2)
        self.board.add_piece(self.rook2)

    def test_check_move(self):
        self.assertIsNotEmpty(self.king.check_piece_valid_move(Position("d1")))
        self.assertIsNotEmpty(self.king.check_piece_valid_move(Position("d2")))
        self.assertIsNotEmpty(self.king.check_piece_valid_move(Position("e2")))
        self.assertIsNotEmpty(self.king.check_piece_valid_move(Position("f1")))
        self.assertIsNotEmpty(self.king.check_piece_valid_move(Position("f2")))
        self.assertIsNotEmpty(self.king.check_piece_valid_move(Position("a1")))
        self.assertIsNotEmpty(self.king.check_piece_valid_move(Position("h1")))
        self.assertIsEmpty(self.king.check_piece_valid_move(Position("e3")))
        self.assertIsEmpty(self.king.check_piece_valid_move(Position("a2")))

    def test_check_moves_same_as_get_valid_moves(self):
        self.piece1 = self.king
        self.piece2 = None
        super().test_check_moves_same_as_get_valid_moves()

    def test_get_valid_moves(self):
        valid_moves = self.king.get_piece_valid_moves()
        self.assertIn(BasicMovement(self.king, Position("e2")), valid_moves)
        self.assertIn(BasicMovement(self.king, Position("f1")), valid_moves)
        self.assertIn(BasicMovement(self.king, Position("f2")), valid_moves)
        self.assertNotIn(BasicMovement(self.king, Position("e3")), valid_moves)

        self.assertIn(Castling(self.king, self.rook1), valid_moves)
        self.assertIn(Castling(self.king, self.rook2), valid_moves)

    def test_king_in_castling_check(self):
        enemy_piece = Rook(self.board, self.other_player, Position("f8"))
        self.board.add_piece(enemy_piece)

        self.assertIsEmpty(self.king.check_piece_valid_move(Position("h1")))
        self.assertIsEmpty(self.king.check_piece_valid_move(Position("g1")))
        self.assertIsNotEmpty(self.king.check_piece_valid_move(Position("a1")))

    def test_piece_in_path(self):
        ally_piece = Empty(self.board, self.main_player, Position("c1"))
        self.board.add_piece(ally_piece)

        self.assertIsEmpty(self.king.check_piece_valid_move(Position("a1")))
        self.assertIsEmpty(self.king.check_piece_valid_move(Position("c1")))
        self.assertIsNotEmpty(self.king.check_piece_valid_move(Position("h1")))

    def test_multidimensional(self):
        self.board = Board((8, 8, 8))

        self.position1 = Position([3, 3, 3])
        self.king = King(self.board, self.main_player, self.position1)
        self.board.add_piece(self.king)

        self.test_check_moves_same_as_get_valid_moves()


if __name__ == '__main__':
    unittest.main()
