import unittest

from ModularChess.GameModes.Classical import Classical
from ModularChess.controller.Player import Player
from ModularChess.pieces.Queen import Queen
from ModularChess.utils.Movement import MovementData
from ModularChess.utils.Position import Position
from ModularChess.utils.Promotion import Promotion


class TestPromotion(unittest.TestCase):

    def setUp(self) -> None:
        self.white = Player("test")
        self.black = Player("test2")

        self.game_mode = Classical(self.white, self.black)

        self.pawn_position = Position([6, 1])
        self.pawn = self.game_mode.ClassicalPawn(self.game_mode.board, self.white, self.pawn_position)
        self.game_mode.board.add_piece(self.pawn)

        self.enemy_piece_position = Position([7, 0])
        self.enemy_piece = Queen(self.game_mode.board, self.black, self.enemy_piece_position)
        self.game_mode.board.add_piece(self.enemy_piece)

        # Basic Promotion
        self.destination1 = Position([7, 1])
        self.promotion1 = Promotion(self.pawn, self.destination1, Queen)
        self.promoted_piece1 = self.promotion1.movements[-1].piece

        # Capture Promotion
        self.promotion2 = Promotion(self.pawn, self.enemy_piece_position, Queen)
        self.promoted_piece2 = self.promotion2.movements[-1].piece

    def test_movements(self):
        self.assertTrue(self.promotion1.check_valid_move())
        self.assertListEqual([MovementData(self.pawn, self.pawn_position, None),
                              MovementData(self.promoted_piece1, None, self.destination1)], self.promotion1.movements)

        self.assertTrue(self.promotion2.check_valid_move())
        self.assertListEqual([MovementData(self.enemy_piece, self.enemy_piece_position, None),
                              MovementData(self.pawn, self.pawn_position, None),
                              MovementData(self.promoted_piece2, None, self.enemy_piece_position)],
                             self.promotion2.movements)

    def test_move1(self):
        self.promotion1.move()
        self.assertEqual(self.promoted_piece1, self.game_mode.board[self.destination1])
        self.assertIsNone(self.game_mode.board[self.pawn_position])
        self.assertListEqual([], self.game_mode.board.pieces[self.white][self.game_mode.ClassicalPawn])
        self.assertListEqual([self.promoted_piece1], self.game_mode.board.pieces[self.white][Queen])
        self.assertEqual(self.pawn.n_moves + 1, self.promoted_piece1.n_moves)

    def test_move2(self):
        self.promotion2.move()
        self.assertEqual(self.promoted_piece2, self.game_mode.board[self.enemy_piece_position])
        self.assertIsNone(self.game_mode.board[self.pawn_position])
        self.assertListEqual([], self.game_mode.board.pieces[self.white][self.game_mode.ClassicalPawn])
        self.assertListEqual([], self.game_mode.board.pieces[self.black][Queen])
        self.assertListEqual([self.promoted_piece2], self.game_mode.board.pieces[self.white][Queen])
        self.assertEqual(self.pawn.n_moves + 1, self.promoted_piece2.n_moves)

    def test_inverse_move(self):
        n_moves = self.pawn.n_moves
        self.promotion1.move()
        self.promotion1.inverse().move()
        self.assertIsNone(self.game_mode.board[self.destination1])
        self.assertEqual(self.pawn, self.game_mode.board[self.pawn_position])
        self.assertEqual(n_moves, self.pawn.n_moves)

        n_moves = self.pawn.n_moves
        self.promotion2.move()
        self.promotion2.inverse().move()
        self.assertEqual(self.enemy_piece, self.game_mode.board[self.enemy_piece_position])
        self.assertEqual(self.pawn, self.game_mode.board[self.pawn_position])
        self.assertEqual(n_moves, self.pawn.n_moves)


if __name__ == '__main__':
    unittest.main()
