import unittest

from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.pieces.Empty import Empty
from ModularChess.utils.Position import Position


class TestBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board(size=10, dimensions=3)
        self.player = Player("test")
        self.piece_position = Position([self.board.size // 2] * self.board.dimensions)
        self.piece = Empty(self.board, self.player, self.piece_position)

    def test_add_piece(self):
        self.board.add_piece(self.piece)

        self.assertEqual(self.piece, self.board[self.piece_position])
        self.assertEqual(self.piece, self.board.pieces[self.player][Empty][0])

    def test_remove_piece(self):
        self.board.add_piece(self.piece)
        self.board.remove_piece(self.piece)

        self.assertIsNone(self.board[self.piece_position])
        self.assertListEqual([], self.board.pieces[self.player][Empty])

    def test_move_piece(self):
        self.board.add_piece(self.piece)
        new_position = Position([0] * self.board.dimensions)
        self.board.move_piece(self.piece, new_position)

        self.assertIsNone(self.board[self.piece_position])
        self.assertEqual(self.piece, self.board[new_position])
        self.assertEqual(self.piece, self.board.pieces[self.player][Empty][0])
        self.assertEqual(1, self.piece.n_moves)

    # TODO
    @unittest.skip("Depends on pieces")
    def test_can_enemy_piece_capture(self):
        self.fail()

    def test_can_capture_or_move(self):
        self.board.add_piece(self.piece)
        new_position = Position([0] * self.board.dimensions)

        self.assertTrue(self.board.can_capture_or_move(self.piece, new_position))
        self.assertFalse(self.board.can_capture_or_move(self.piece, self.piece_position))

        player2 = Player("2")
        piece_position2 = Position([self.board.size - 1] * self.board.dimensions)
        piece2 = Empty(self.board, player2, piece_position2)
        self.board.add_piece(piece2)

        self.assertTrue(self.board.can_capture_or_move(self.piece, piece_position2))
        self.assertTrue(self.board.can_capture_or_move(piece2, self.piece_position))

        Player.join_allies([self.player, player2])

        self.assertFalse(self.board.can_capture_or_move(self.piece, piece_position2))
        self.assertFalse(self.board.can_capture_or_move(piece2, self.piece_position))

    def test_is_an_enemy_piece(self):
        self.board.add_piece(self.piece)
        player2 = Player("2")
        piece_position2 = Position([self.board.size - 1] * self.board.dimensions)
        piece2 = Empty(self.board, player2, piece_position2)
        self.board.add_piece(piece2)

        self.assertTrue(self.board.is_an_enemy_piece(self.piece, piece_position2))
        self.assertTrue(self.board.is_an_enemy_piece(piece2, self.piece_position))

        Player.join_allies([self.player, player2])

        self.assertFalse(self.board.is_an_enemy_piece(self.piece, piece_position2))
        self.assertFalse(self.board.is_an_enemy_piece(piece2, self.piece_position))

    def test_is_position_outside(self):
        test1 = Position([self.board.size * 10] * self.board.dimensions)
        self.assertTrue(self.board.is_position_outside(test1))

        test2 = Position([-1] * self.board.dimensions)
        self.assertTrue(self.board.is_position_outside(test2))

        self.assertFalse(self.board.is_position_outside(self.piece_position))

    def test_is_position_inside(self):
        test1 = Position([self.board.size * 10] * self.board.dimensions)
        self.assertFalse(self.board.is_position_inside(test1))

        test2 = Position([-1] * self.board.dimensions)
        self.assertFalse(self.board.is_position_inside(test2))

        self.assertTrue(self.board.is_position_inside(self.piece_position))


if __name__ == '__main__':
    unittest.main()
