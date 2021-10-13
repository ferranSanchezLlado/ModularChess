import os
from typing import List, TYPE_CHECKING, TextIO

import numpy as np
import numpy.typing as npt

import ModularChess.pieces.Rook as Rook
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Castling import CastlablePiece, Castling
from ModularChess.utils.Position import Position

if TYPE_CHECKING:
    from ModularChess.utils.Movement import Movement
    from ModularChess.controller.Player import Player
    from ModularChess.controller.Board import Board


class King(CastlablePiece):

    def __init__(self, board: "Board", player: "Player", starting_position: "Position"):
        super().__init__(board, player, starting_position, [Rook.Rook])

    def find_castling_destination(self, other_piece: "CastlablePiece") -> "Position":
        direction: "Position" = other_piece.position - self.position
        if self.n_moves != 0 or other_piece.n_moves != 0:
            raise Exception("Piece has moved")
        if np.any(self.position[~(direction != 0)] != other_piece.position[~(direction != 0)]):
            raise Exception("Invalid Axis")

        destination: "Position" = self.position + np.ceil(direction / 2).astype(np.int_)
        return destination

    def check_valid_castling_destination(self, destination: "Position", other_piece: "CastlablePiece") -> bool:

        if self.n_moves or other_piece.n_moves:
            return False

        # Checks pieces in the path
        try:
            if any(list(self.board[pos] for pos in self.position.create_lineal_path(other_piece.position))[:-1]):
                return False
        except Exception:
            return False

        # Checks during the path of the king
        if any(self.board.can_enemy_piece_capture_position(pos, self.player) for pos in
               self.position.create_lineal_path(destination)):
            return False

        return True

    # TODO: Castling
    # TODO: Checks
    def check_move(self, new_position: "Position") -> List["Movement"]:
        # Piece didn't move or outside board
        if super().check_move(new_position) is None:
            return []
        diff = np.abs(new_position - self.position)

        # Moves more than one in axis
        if np.any(diff > 1):
            try:
                piece = self.find_nearest_piece(new_position)
                destination = self.find_castling_destination(piece)
                if self.check_valid_castling_destination(destination, piece):
                    return [Castling(self, piece)]
            except Exception:
                pass
            return []

        # Checks if destination is not empty or there is an enemy piece
        if not self.board.can_capture_or_move(self, new_position):
            return []
        return [BasicMovement(self, new_position)]

    def get_valid_moves(self) -> List["Movement"]:
        moves: List["Movement"] = []

        for i in range(1, 2 ** len(self.position)):
            binary = [int(x) for x in bin(i)[2:]]
            vector: npt.NDArray[np.int_] = np.array([0] * (len(self.position) - len(binary)) + binary)

            n_1s: npt.NDArray[np.bool_] = vector == 1
            for j in range(2 ** np.sum(n_1s)):
                binary = [int(x) for x in bin(j)[2:]]
                direction: npt.NDArray[np.int_] = np.array([0] * (sum(n_1s) - len(binary)) + binary)

                vector[n_1s] = np.where(direction == 1, -1, 1)
                position: Position = Position(vector) + self.position
                if self.board.is_position_inside(position) and self.board.can_capture_or_move(self, position):
                    moves.append(BasicMovement(self, position))

        # Finds possible castling positions
        if self.n_moves == 0:
            for piece in self.get_possible_castlable_pieces():
                move = Castling(self, piece)
                if move.check_valid_move():
                    moves.append(move)
        return moves

    @staticmethod
    def piece_unicode() -> str:
        return "♔"

    @staticmethod
    def abbreviation() -> str:
        return "K"

    @staticmethod
    def image() -> TextIO:
        return open(os.path.join(King.res_path, "King.png"))
