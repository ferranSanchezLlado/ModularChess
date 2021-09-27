from typing import List

import numpy as np

from ModularChess.pieces.Piece import Piece
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Movement import Movement
from ModularChess.utils.Position import Position


class Empty(Piece):

    def check_move(self, new_position: Position) -> bool:
        return True

    def get_valid_moves(self) -> List[Movement]:
        moves: List[Movement] = []
        for index in np.ndindex(self.board.board.shape):
            moves.append(BasicMovement(self, Position(index)))
        return []

    def __repr__(self) -> str:
        return "▣"
