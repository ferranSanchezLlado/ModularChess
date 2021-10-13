import unittest

from ModularChess.GameModes.Classical import Classical
from ModularChess.controller.Player import Player
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.EnPassant import EnPassant
from ModularChess.utils.Position import Position
from ModularChess.utils.Promotion import Promotion
from tests.pieces.base_test_pieces import BaseTestPieces


class TestClassicalPawn(BaseTestPieces):
    __test__ = True

    def setUp(self) -> None:
        self.main_player = Player("White")
        self.other_player = Player("Black")
        self.game_mode = Classical(self.main_player, self.other_player)
        self.board = self.game_mode.board
        self.Pawn = self.game_mode.ClassicalPawn

        self.position1 = Position("b2")
        self.piece1 = self.Pawn(self.board, self.main_player, self.position1)
        self.board.add_piece(self.piece1)

        self.position2 = Position("e7")
        self.piece2 = self.game_mode.ClassicalPawn(self.board, self.main_player, self.position2)
        self.board.add_piece(self.piece2)

    def test_check_move(self):
        self.assertIsNotEmpty(self.piece1.check_move(Position("b3")))
        self.assertIsNotEmpty(self.piece1.check_move(Position("b4")))
        self.assertIsEmpty(self.piece1.check_move(Position("a3")))
        self.assertIsEmpty(self.piece1.check_move(Position("c3")))
        self.assertIsEmpty(self.piece1.check_move(Position("b5")))
        self.assertIsEmpty(self.piece1.check_move(Position("b1")))

        position = Position("e8")
        promotion = self.piece2.check_move(position)
        self.assertIsNotEmpty(promotion)
        self.assertListEqual([Promotion(self.piece2, position, piece_type) for piece_type in
                              self.piece2.valid_pieces_type], promotion)
        self.assertIsEmpty(self.piece2.check_move(Position("d8")))
        self.assertIsEmpty(self.piece2.check_move(Position("f8")))

    def test_get_valid_moves(self):
        valid_moves = self.piece1.get_valid_moves()
        self.assertListEqual([BasicMovement(self.piece1, Position("b3")), BasicMovement(self.piece1, Position("b4"))],
                             valid_moves)

        valid_moves = self.piece2.get_valid_moves()
        self.assertListEqual([Promotion(self.piece2, Position("e8"), piece_type) for piece_type in
                              self.piece2.valid_pieces_type], valid_moves)

    def test_capture(self):
        position = Position("a3")
        enemy_piece = self.Pawn(self.board, self.other_player, position)
        self.board.add_piece(enemy_piece)

        self.assertIsNotEmpty(self.piece1.check_move(position))
        self.assertIn(BasicMovement(self.piece1, position), self.piece1.get_valid_moves())

        position = Position("f8")
        enemy_piece = self.Pawn(self.board, self.other_player, position)
        self.board.add_piece(enemy_piece)

        self.assertIsNotEmpty(self.piece2.check_move(position))
        self.assertIn(Promotion(self.piece2, position, self.piece2.valid_pieces_type[0]), self.piece2.get_valid_moves())

    def test_piece_in_front(self):
        position = Position("b3")
        self.board.add_piece(self.Pawn(self.board, self.other_player, position))

        self.assertIsEmpty(self.piece1.check_move(position))
        self.assertIsEmpty(self.piece1.get_valid_moves())

        self.setUp()
        position = Position("b4")
        self.board.add_piece(self.Pawn(self.board, self.other_player, position))

        self.assertIsEmpty(self.piece1.check_move(position))
        self.assertIsNotEmpty(self.piece1.check_move(Position("b3")))
        self.assertEqual([BasicMovement(self.piece1, Position("b3"))], self.piece1.get_valid_moves())

        position = Position("e8")
        self.board.add_piece(self.Pawn(self.board, self.other_player, position))

        self.assertIsEmpty(self.piece2.check_move(position))
        self.assertIsEmpty(self.piece2.get_valid_moves())

    def test_check_moves_same_as_get_valid_moves(self):
        super().test_check_moves_same_as_get_valid_moves()

    def test_en_passant(self):
        position = Position("e5")
        main_piece = self.Pawn(self.board, self.main_player, position)
        main_piece.n_moves = 2
        self.board.add_piece(main_piece)

        other_position = Position("f7")
        other_piece = self.Pawn(self.board, self.other_player, other_position)
        self.board.add_piece(other_piece)

        self.game_mode.turn = next(self.game_mode.order)
        self.game_mode.force_move(other_piece.check_move(Position("f5"))[0])

        self.assertIsNotEmpty(main_piece.check_move(Position("f6")))
        self.assertIn(EnPassant(main_piece, Position("f6"), other_piece), main_piece.get_valid_moves())
        self.assertIsEmpty(main_piece.check_move(Position("d6")))

        other_piece.n_moves = 2
        self.assertIsEmpty(main_piece.check_move(Position("f6")))

    @unittest.skip("Multidimensional not implemented")
    def test_multidimensional(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
