from typing import List

import numpy as np
import numpy.typing as npt

import ModularChess.pieces.Rook as Rook
from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Castling import CastlablePiece, Castling
from ModularChess.utils.Movement import Movement
from ModularChess.utils.Position import Position


class King(CastlablePiece):

    def __init__(self, board: "Board", player: Player, starting_position: Position):
        super(King, self).__init__(board, player, starting_position, [Rook.Rook])

    def find_castling_destination(self, other_piece: "CastlablePiece") -> Position:
        direction: Position = other_piece.position - self.position
        if self.position[~(direction != 0)] != other_piece.position[~(direction != 0)]:
            raise Exception("Invalid Axis")

        destination: Position = self.position + np.ceil(direction / 2).astype(np.int_)
        return destination

    def check_valid_castling_destination(self, destination: Position, other_piece: "CastlablePiece") -> bool:

        if self.n_moves or other_piece.n_moves:
            return False

        # Checks pieces in the path
        if any(list(self.board[pos] for pos in self.position.create_lineal_path(other_piece.position))[:-1]):
            return False

        # Checks during the path of the king
        if any(self.board.can_enemy_piece_capture(pos, self.player) for pos in
               self.position.create_lineal_path(destination)):
            return False
        return True

    # TODO: Castling
    # TODO: Checks
    def check_move(self, new_position: Position) -> bool:
        # Piece didn't move or outside board
        if not super().check_move(new_position):
            return False
        diff = np.abs(new_position - self.position)

        # Moves more than one in axis
        if np.any(diff > 1):
            try:
                piece = self.find_nearest_piece(new_position)
                destination = self.find_castling_destination(piece)
                if self.check_valid_castling_destination(destination, piece):
                    return True
            except Exception:
                pass
            return False

        # Checks if destination is empty or there is an enemy piece
        return self.board.can_capture_or_move(self, new_position)

    def get_valid_moves(self) -> List[Movement]:
        moves: List[Movement] = []

        for i in range(1, 2**len(self.position)):
            binary = [int(x) for x in bin(i)[2:]]
            vector: npt.NDArray[np.int_] = np.array([0] * (len(self.position) - len(binary)) + binary)

            n_1s: npt.NDArray[np.bool_] = vector == 1
            for j in range(2 ** np.sum(n_1s)):
                binary = [int(x) for x in bin(j)[2:]]
                direction: npt.NDArray[np.int_] = np.array([0] * (sum(n_1s) - len(binary)) + binary)

                vector[n_1s] = np.where(direction == 1, -1, 1)
                position: Position = Position(vector) + self.position
                if self.__can_move_to__(position):
                    moves.append(BasicMovement(self, position))

        # Finds possible castling positions
        for piece in self.get_possible_castlable_pieces():
            move = Castling(self, piece)
            if move.check_valid_move():
                moves.append(move)
        return moves

    def __repr__(self) -> str:
        return "♔"
