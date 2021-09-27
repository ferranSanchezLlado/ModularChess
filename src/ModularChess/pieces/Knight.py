import itertools
from typing import List

import numpy as np

from ModularChess.pieces.Piece import Piece
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Movement import Movement
from ModularChess.utils.Position import Position


class Knight(Piece):

    def check_move(self, new_position: Position) -> bool:
        if not super(Knight, self).check_move(new_position):
            return False

        diff = np.abs(new_position - self.position)
        return sum(diff == 2) == 1 and sum(diff == 1) == 1 and sum(diff == 0) == self.board.dimensions - 2 and (
            self.board.can_capture_or_move(self, new_position))

    def get_valid_moves(self) -> List[Movement]:
        moves: List[Movement] = []

        for a, b in itertools.permutations(np.identity(self.board.dimensions, dtype=int), 2):

            # Transforms binary inputs to integer and checks a > b. Avoiding already seen permutations
            if a.dot(2 ** np.arange(a.size)[::-1]) > b.dot(2 ** np.arange(b.size)[::-1]):
                for i in [-2, 2]:
                    for j in [-1, 1]:
                        for move in (Position(i * a + j * b), Position(j * a + i * b)):
                            move += self.position
                            if self.board.is_position_inside(move) and self.board.can_capture_or_move(self, move):
                                moves.append(BasicMovement(self, move))
        return moves

    def __repr__(self) -> str:
        return "♘"
