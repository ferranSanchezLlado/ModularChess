import unittest
from typing import List, Optional

from ModularChess.GameModes.Classical import Classical
from ModularChess.controller.Player import Player
from ModularChess.pieces.King import King
from ModularChess.pieces.Queen import Queen
from ModularChess.pieces.Rook import Rook
from ModularChess.utils.Castling import Castling
from ModularChess.utils.Movement import MovementData, Movement
from ModularChess.utils.Position import Position


class DebugMovement(Movement):

    def __init__(self, movements: List[MovementData], player: Optional[Player] = None):
        super(DebugMovement, self).__init__(movements, player)


class TestCastling(unittest.TestCase):

    def setUp(self) -> None:
        self.white = Player("test")
        self.black = Player("test2")

        self.game_mode = Classical(self.white, self.black)

        self.king_position = Position("e1")
        self.king = King(self.game_mode.board, self.white, self.king_position)
        self.game_mode.board.add_piece(self.king)

        self.rook_position1 = Position("a1")
        self.rook1 = Rook(self.game_mode.board, self.white, self.rook_position1)
        self.game_mode.board.add_piece(self.rook1)

        self.rook_position2 = Position("h1")
        self.rook2 = Rook(self.game_mode.board, self.white, self.rook_position2)
        self.game_mode.board.add_piece(self.rook2)

        self.castling1 = Castling(self.king, self.rook1)
        self.castling2 = Castling(self.king, self.rook2)

    def test_movements(self):
        self.assertTrue(self.castling1.check_valid_move())

        truth1 = DebugMovement([MovementData(self.king, self.king_position, Position("c1")),
                                MovementData(self.rook1, self.rook_position1, Position("d1"))])
        self.assertEqual(truth1, self.castling1)

        self.assertTrue(self.castling2.check_valid_move())

        truth2 = DebugMovement([MovementData(self.king, self.king_position, Position("g1")),
                                MovementData(self.rook2, self.rook_position2, Position("f1"))])
        self.assertEqual(truth2, self.castling2)

    def test_move1(self):
        self.castling1.move()
        self.assertEqual(self.king, self.game_mode.board[Position("c1")])
        self.assertEqual(self.rook1, self.game_mode.board[Position("d1")])
        self.assertEqual(1, self.king.n_moves)
        self.assertEqual(self.king.n_moves, self.rook1.n_moves)

    def test_move2(self):
        self.castling2.move()
        self.assertEqual(self.king, self.game_mode.board[Position("g1")])
        self.assertEqual(self.rook2, self.game_mode.board[Position("f1")])
        self.assertEqual(1, self.king.n_moves)
        self.assertEqual(self.king.n_moves, self.rook2.n_moves)

    def test_inverse_move(self):
        n_moves = self.king.n_moves
        self.castling1.move()
        self.castling1.inverse().move()
        self.assertIsNone(self.game_mode.board[Position("c1")])
        self.assertIsNone(self.game_mode.board[Position("d1")])
        self.assertEqual(self.king, self.game_mode.board[self.king_position])
        self.assertEqual(self.rook1, self.game_mode.board[self.rook_position1])
        self.assertEqual(n_moves, self.king.n_moves)
        self.assertEqual(n_moves, self.rook1.n_moves)

        n_moves = self.king.n_moves
        self.castling2.move()
        self.castling2.inverse().move()
        self.assertIsNone(self.game_mode.board[Position("g1")])
        self.assertIsNone(self.game_mode.board[Position("f1")])
        self.assertEqual(self.king, self.game_mode.board[self.king_position])
        self.assertEqual(self.rook2, self.game_mode.board[self.rook_position2])
        self.assertEqual(n_moves, self.king.n_moves)
        self.assertEqual(n_moves, self.rook2.n_moves)

    def test_king_in_check_during_move(self):
        enemy_piece1 = Queen(self.game_mode.board, self.black, Position("d5"))
        self.game_mode.board.add_piece(enemy_piece1)

        self.assertFalse(self.castling1.check_valid_move())
        self.assertTrue(self.castling2.check_valid_move())  # Rook is attacked

    def test_piece_in_path(self):
        other = Queen(self.game_mode.board, self.white, Position("d1"))
        self.game_mode.board.add_piece(other)

        self.assertFalse(self.castling1.check_valid_move())
        self.assertTrue(self.castling2.check_valid_move())

    def test_nearest_piece(self):
        nearest = self.king.find_nearest_piece(Position("g1"))
        self.assertEqual(self.rook2, nearest)

        self.assertRaises(Exception, self.king.find_nearest_piece, Position("f2"))


if __name__ == '__main__':
    unittest.main()
