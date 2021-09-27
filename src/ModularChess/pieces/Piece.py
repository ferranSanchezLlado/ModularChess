import abc
from typing import TYPE_CHECKING

import numpy as np

from ModularChess.controller.Player import Player
from ModularChess.utils.Position import Position

if TYPE_CHECKING:
    from ModularChess.utils.Movement import Movement
    from ModularChess.controller.Board import Board


# TODO: Abstract classes or variable for Special movement
class Piece(metaclass=abc.ABCMeta):

    def __init__(self, board: "Board", player: Player, starting_position: Position):
        self.player = player
        self.board = board
        self.position = starting_position  # TODO: Change to Optional

        self.n_moves = 0
        self._a_piece_already_captured_ = False  # Initializes private variable

    @abc.abstractmethod
    def check_move(self, new_position: Position) -> bool:
        """
        Checks if the piece can be moved to the specified position. The moves to be tested should represent
        BasicMovement, allowing the testing through Movement.

        :param new_position: destination of the piece
        :return: True if move is valid
        """
        return not np.array_equal(self.position, new_position) and self.board.is_position_inside(new_position)

    @abc.abstractmethod
    def get_valid_moves(self) -> "list[Movement]":
        # TODO: Filter moves that leave king in check
        return []

    def __can_move_to__(self, position: Position):
        if self._a_piece_already_captured_:
            self._a_piece_already_captured_ = False  # Restarts variable
            return False
        piece = self.board[position]
        if piece is not None:
            if self.player == piece.player:
                return False
            self._a_piece_already_captured_ = True
        return True
