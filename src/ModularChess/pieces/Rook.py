import os
from typing import List, TYPE_CHECKING, TextIO

import numpy as np

import ModularChess.pieces.King as King
from ModularChess.movements.BasicMovement import BasicMovement
from ModularChess.movements.Castling import CastlablePiece
from ModularChess.utils.Exceptions import InvalidMoveException

if TYPE_CHECKING:
    from ModularChess.controller.Board import Board
    from ModularChess.controller.Player import Player
    from ModularChess.pieces.Piece import Piece
    from ModularChess.movements.Movement import Movement
    from ModularChess.utils.Position import Position


class Rook(CastlablePiece):

    def __init__(self, board: "Board", player: "Player", starting_position: "Position"):
        super().__init__(board, player, starting_position, [King.King])

    def find_castling_destination(self, other_piece: "CastlablePiece") -> "Position":
        direction: "Position" = other_piece.position - self.position
        if self.position[~(direction != 0)] != other_piece.position[~(direction != 0)]:
            raise InvalidMoveException("Invalid Axis")

        destination: "Position" = self.position + np.ceil(direction / 2).astype(np.int_) + (
            np.floor_divide(np.abs(direction), direction, out=np.zeros_like(direction), where=direction != 0))
        return destination

    def check_valid_castling_destination(self, destination: "Position", other_piece: "CastlablePiece") -> bool:
        # Checked in King
        return True

    def check_piece_valid_move(self, new_position: "Position") -> List["Movement"]:
        # Piece didn't move or outside board
        if super().check_piece_valid_move(new_position) is None:
            return []
        return Rook.lineal_check_move(self, new_position)

    def get_piece_valid_moves(self) -> List["Movement"]:
        return Rook.get_rook_valid_moves(self)

    @classmethod
    def get_rook_valid_moves(cls, piece: "Piece") -> List["Movement"]:
        # TODO: Redo
        moves: List["Movement"] = []

        for i, max_index in enumerate(piece.board.shape):
            min_iterable = piece.position.create_lineal_path(piece.position.copy_and_replace(i, 0))
            moves += [BasicMovement(piece, pos, is_valid_move=True) for pos in piece.__can_move_to__(min_iterable)]
            max_iterable = piece.position.create_lineal_path(piece.position.copy_and_replace(i, max_index))
            moves += [BasicMovement(piece, pos, is_valid_move=True) for pos in piece.__can_move_to__(max_iterable)]

        return moves

    @classmethod
    def lineal_check_move(cls, piece: "Piece", new_position: "Position") -> List["Movement"]:
        diff: "Position" = new_position - piece.position
        axis_diff = diff != 0

        n_axis_diff = np.sum(axis_diff)

        # Moves in only one axis
        if n_axis_diff != 1:
            return []

        # Checks pieces in the path
        if any([piece.board[pos] for pos in piece.position.create_lineal_path(new_position)][:-1]):
            return []

        # Checks if destination is not empty or there is an enemy piece
        if not piece.board.can_capture_or_move(piece, new_position):
            return []
        return [BasicMovement(piece, new_position, is_valid_move=True)]

    @staticmethod
    def piece_unicode() -> str:
        return "???"

    @staticmethod
    def abbreviation() -> str:
        return "R"

    @staticmethod
    def image() -> TextIO:
        return open(os.path.join(Rook.res_path, "Rook.png"))

    @staticmethod
    def piece_value() -> float:
        return 5
