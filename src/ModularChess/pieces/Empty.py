from typing import List, TYPE_CHECKING, TextIO

import numpy as np

from ModularChess.movements.BasicMovement import BasicMovement
from ModularChess.pieces.Piece import Piece
from ModularChess.utils.Position import Position

if TYPE_CHECKING:
    from ModularChess.movements.Movement import Movement


class Empty(Piece):

    def check_piece_valid_move(self, new_position: "Position") -> List["Movement"]:
        return [BasicMovement(self, new_position, is_valid_move=True)]

    def get_piece_valid_moves(self) -> List["Movement"]:
        moves: List["Movement"] = []
        for index in np.ndindex(*self.board.shape):
            moves.append(BasicMovement(self, Position(index), is_valid_move=True))
        return []

    @staticmethod
    def piece_unicode() -> str:
        return "▣"

    @staticmethod
    def abbreviation() -> str:
        return "None"

    @staticmethod
    def image() -> TextIO:
        raise NotImplementedError("No image")

    @staticmethod
    def piece_value() -> float:
        raise NotImplementedError("Doesn't have a value")
