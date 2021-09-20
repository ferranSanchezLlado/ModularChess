from typing import List

import numpy as np
import numpy.typing as npt

from src.ModularChess.pieces.Piece import Piece
from src.ModularChess.utils.BasicMovement import BasicMovement
from src.ModularChess.utils.Movement import Movement
from src.ModularChess.utils.Position import Position


class King(Piece):

    # TODO: Castling
    # TODO: Checks
    def check_move(self, new_position: Position) -> bool:
        # Piece didn't move or outside board
        if not super().check_move(new_position):
            return False
        diff = np.abs(new_position - self.position)

        # Moves more than one in axis
        if np.any(diff > 1):
            return False

        # Checks if destination is empty or there is an enemy piece
        return self.board.can_capture_or_move(self, new_position)

    def get_valid_moves(self) -> List[Movement]:
        moves: List[Movement] = []

        for i in range(1, 2**len(self.position)):
            binary = [int(x) for x in bin(i)[2:]]
            vector: npt.NDArray[np.int_] = np.array([0] * (len(self.position) - len(binary)) + binary)

            n_1s: npt.NDArray[np.bool_] = vector == 1
            for j in range(2**np.sum(n_1s)):
                binary = [int(x) for x in bin(j)[2:]]
                direction: npt.NDArray[np.int_] = np.array([0] * (sum(n_1s) - len(binary)) + binary)

                vector[n_1s] = np.where(direction == 1, -1, 1)
                position: Position = Position(vector) + self.position
                if self.__can_move_to__(position):
                    moves.append(BasicMovement(self, position))

        # TODO: Castling
        return moves

    def __repr__(self) -> str:
        return "♔"
