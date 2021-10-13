import abc
import unittest
from typing import Type, List

import numpy as np

from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.pieces.Piece import Piece
from ModularChess.utils.Movement import Movement
from ModularChess.utils.Position import Position


class BaseTestPieces(unittest.TestCase, abc.ABC):
    __test__ = False

    def custom_setUp(self, piece_type: Type[Piece], position1: Position, position2: Position) -> None:
        self.board = Board()
        self.main_player = Player("White")
        self.other_player = Player("Black")

        players = [self.main_player, self.other_player]
        Player.join_allies([self.main_player], players)
        Player.join_allies([self.other_player], players)

        self.position1 = position1
        self.piece1 = piece_type(self.board, self.main_player, position1)
        self.board.add_piece(self.piece1)

        self.position2 = position2
        self.piece2 = piece_type(self.board, self.main_player, position2)
        self.board.add_piece(self.piece2)

    def test_check_moves_same_as_get_valid_moves(self):
        for piece in (self.piece1, self.piece2):
            if piece is not None:
                check_valid_moves_list: List[Movement] = []
                for pos in np.ndindex(*self.board.shape):
                    moves = piece.check_move(Position(pos))
                    if moves is not None:
                        check_valid_moves_list += moves

                get_valid_moves_list = piece.get_valid_moves()
                for move in check_valid_moves_list:
                    if move not in get_valid_moves_list:
                        self.fail(move)

    def assertIsEmpty(self, a: List):
        self.assertEqual([], a)

    def assertIsNotEmpty(self, a: List):
        self.assertNotEqual([], a)
