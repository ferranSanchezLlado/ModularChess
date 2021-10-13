import itertools
import os
from typing import List, TYPE_CHECKING, TextIO

import numpy as np
import numpy.typing as npt

from ModularChess.pieces.Piece import Piece
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Position import Position

if TYPE_CHECKING:
    from ModularChess.utils.Movement import Movement


class Bishop(Piece):

    def check_move(self, new_position: "Position") -> List["Movement"]:
        # Piece didn't move or outside board
        if super().check_move(new_position) is None:
            return []
        return Bishop.two_lineal_check_move(self, new_position)

    def get_valid_moves(self) -> List["Movement"]:
        return Bishop.get_bishop_valid_moves(self)

    @classmethod
    def get_bishop_valid_moves(cls, piece: "Piece") -> List["Movement"]:
        moves: List["Movement"] = []

        for a, b in itertools.permutations(np.identity(piece.board.dimensions, dtype=int), 2):

            # Transforms binary inputs to integer and checks a > b. Avoiding already seen permutations
            if a.dot(2 ** np.arange(a.size)[::-1]) > b.dot(2 ** np.arange(b.size)[::-1]):
                vector: npt.NDArray[np.int_] = a + b

                for direction in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                    # Changes vector to the possible 4 directions in 2D
                    index = np.where(vector)
                    vector[index] = direction

                    direction_array: npt.NDArray[np.int_] = np.array(list(piece.board.size - 1 if el > 0 else 0 for el
                                                                          in direction))
                    magnitude: npt.NDArray[np.int_] = np.min(np.abs(direction_array - piece.position[index]))

                    end_position: Position = Position(piece.position + magnitude * vector)

                    min_iterable = piece.position.create_lineal_path(end_position)
                    moves += [BasicMovement(piece, pos) for pos in piece.__can_move_to__(min_iterable)]

        return moves

    # noinspection PyTypeChecker
    @classmethod
    def two_lineal_check_move(cls, piece: "Piece", new_position: "Position") -> List["Movement"]:
        diff: "Position" = new_position - piece.position
        axis_diff: "Position" = diff != 0
        n_axis_diff: "Position" = np.sum(axis_diff)
        abs_diff_axis: "Position" = np.abs(diff[axis_diff])

        # Moves in only two axis
        if n_axis_diff != 2 or np.max(abs_diff_axis) != np.min(abs_diff_axis):
            return []

        # Checks pieces in the path
        if any(list(piece.board[pos] for pos in piece.position.create_lineal_path(new_position))[:-1]):
            return []

        # Checks if destination is not empty or there is an enemy piece
        if piece.board.can_capture_or_move(piece, new_position):
            return [BasicMovement(piece, new_position)]
        return []

    @staticmethod
    def piece_unicode() -> str:
        return "♗"

    @staticmethod
    def abbreviation() -> str:
        return "B"

    @staticmethod
    def image() -> TextIO:
        return open(os.path.join(Bishop.res_path, "Bishop.png"))
