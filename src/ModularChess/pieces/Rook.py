import itertools
from typing import List

import numpy as np

from src.ModularChess.pieces.Piece import Piece
from src.ModularChess.utils.BasicMovement import BasicMovement
from src.ModularChess.utils.Movement import Movement
from src.ModularChess.utils.Position import Position


class Rook(Piece):

    def check_move(self, new_position: Position) -> bool:
        # Piece didn't move or outside board
        if not super().check_move(new_position):
            return False
        return Rook.lineal_check_move(self, new_position)

    def get_valid_moves(self) -> List[Movement]:
        return Rook.get_rook_valid_moves(self)

    @classmethod
    def get_rook_valid_moves(cls, piece: Piece) -> List[Movement]:
        moves: List[Movement] = []

        for i in range(len(piece.position)):

            min_iterable = piece.position.create_lineal_path(piece.position.copy_and_replace(i, 0))
            moves += [BasicMovement(piece, pos) for pos in itertools.takewhile(piece.__can_move_to__, min_iterable)]
            max_iterable = piece.position.create_lineal_path(piece.position.copy_and_replace(i, piece.board.size - 1))
            moves += [BasicMovement(piece, pos) for pos in itertools.takewhile(piece.__can_move_to__, max_iterable)]

        return moves

    @classmethod
    def lineal_check_move(cls, piece: Piece, new_position: Position) -> bool:
        diff: Position = new_position - piece.position
        axis_diff = diff != 0

        n_axis_diff = np.sum(axis_diff)

        # Moves in only one axis
        if n_axis_diff != 1:
            return False

        # Checks pieces in the path
        if any(list(piece.board[pos] for pos in piece.position.create_lineal_path(new_position))[:-1]):
            return False

        # Checks if destination is empty or there is an enemy piece
        return piece.board.can_capture_or_move(piece, new_position)

    def __repr__(self) -> str:
        return "♖"
