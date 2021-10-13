from typing import List, TYPE_CHECKING, TextIO

import numpy as np

from ModularChess.pieces.Piece import Piece
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Position import Position

if TYPE_CHECKING:
    from ModularChess.utils.Movement import Movement


class Empty(Piece):

    def check_move(self, new_position: "Position") -> List["Movement"]:
        return [BasicMovement(self, new_position)]

    def get_valid_moves(self) -> List["Movement"]:
        moves: List["Movement"] = []
        for index in np.ndindex(*self.board.shape):
            moves.append(BasicMovement(self, Position(index)))
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
