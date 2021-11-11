import unittest

from ModularChess.controller.Player import Player
from ModularChess.game_modes.Classical import Classical
from ModularChess.movements.BasicMovement import BasicMovement
from ModularChess.movements.EnPassant import EnPassant
from ModularChess.movements.Movement import MovementData
from ModularChess.pieces.Piece import Piece
from ModularChess.utils.Position import Position


class TestPromotion(unittest.TestCase):

    def setUp(self) -> None:
        self.player1 = Player("test")
        self.player2 = Player("test2")

        self.game_mode = Classical(self.player1, self.player2)
        self.game_mode.generate_board()
        self.board = self.game_mode.board

        self.piece_position1 = Position("a4")
        self.piece1: Piece = self.game_mode.ClassicalPawn(self.board, self.player1, self.piece_position1)

        self.piece_position2 = Position("b7")
        self.piece2: Piece = self.game_mode.ClassicalPawn(self.board, self.player2, self.piece_position2)

        self.board.add_piece(self.piece1)
        self.board.add_piece(self.piece2)

        initial_move = BasicMovement(self.piece1, Position("a5"))
        self.game_mode.force_move(initial_move)

        initial_move = BasicMovement(self.piece2, Position("b5"))
        self.game_mode.force_move(initial_move)

    def test_move(self):
        move = EnPassant(self.piece1, Position("b6"), self.piece2)

        self.assertTrue(move.check_valid_move())
        self.assertTupleEqual(((MovementData(self.piece2, Position("b5"), None),
                                MovementData(self.piece1, Position("a5"), Position("b6")))), move.movements)
        self.assertEqual(self.piece1.check_piece_valid_move(Position("b6"))[0], move)

    def test_move_to_capture(self):
        self.piece2.n_moves = 2
        move = EnPassant(self.piece1, Position("b6"), self.piece2)

        self.assertFalse(move.check_valid_move())
        self.assertEqual([], self.piece1.check_piece_valid_move(Position("b6")))


if __name__ == '__main__':
    unittest.main()
