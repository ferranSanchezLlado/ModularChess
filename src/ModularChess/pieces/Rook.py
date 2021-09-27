import itertools
from typing import List

import numpy as np

import ModularChess.pieces.King as King
from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.pieces.Piece import Piece
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Castling import CastlablePiece
from ModularChess.utils.Movement import Movement
from ModularChess.utils.Position import Position


class Rook(CastlablePiece):

    def __init__(self, board: "Board", player: Player, starting_position: Position):
        super(Rook, self).__init__(board, player, starting_position, [King.King])

    def find_castling_destination(self, other_piece: "CastlablePiece") -> Position:
        direction: Position = other_piece.position - self.position
        if self.position[~(direction != 0)] != other_piece.position[~(direction != 0)]:
            raise Exception("Invalid Axis")

        destination: Position = self.position + np.ceil(direction / 2).astype(np.int_) + \
            np.floor_divide(np.abs(direction), direction, out=np.zeros_like(direction), where=direction != 0)
        return destination

    def check_valid_castling_destination(self, destination: Position, other_piece: "CastlablePiece") -> bool:
        # Checked in King
        return True

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
