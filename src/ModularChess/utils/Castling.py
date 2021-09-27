import abc
from typing import Type, List, cast, Optional

import numpy as np

from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.pieces.Piece import Piece
from ModularChess.utils.Movement import Movement, MovementData
from ModularChess.utils.Position import Position


class CastlablePiece(Piece, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, board: "Board", player: Player, starting_position: Position,
                 castlable_pieces: Optional[List[Type["CastlablePiece"]]] = None):
        super().__init__(board, player, starting_position)
        self.castlable_pieces: List[Type["CastlablePiece"]] = castlable_pieces or \
                                                              [piece_type for piece_type in board.pieces[player].keys()
                                                               if issubclass(piece_type, CastlablePiece)]

    def get_possible_castlable_pieces(self) -> List["CastlablePiece"]:
        return [cast(CastlablePiece, piece) for piece_type in self.castlable_pieces for piece in
                self.board.pieces[self.player][piece_type]]

    def find_nearest_piece(self, aprox_direction: Position) -> "CastlablePiece":
        possible_castlable_pieces = self.get_possible_castlable_pieces()

        direction: Position = aprox_direction - self.position

        # Checks if direction is only in one axis
        if np.sum(direction != 0) != 1:
            raise Exception("Invalid Move")
        dir_pieces = np.abs([np.sum(piece.position - aprox_direction) for piece in possible_castlable_pieces])
        nearest_piece = possible_castlable_pieces[np.argmin(dir_pieces)]

        return nearest_piece

    @abc.abstractmethod
    def find_castling_destination(self, other_piece: "CastlablePiece") -> Position:
        pass

    @abc.abstractmethod
    def check_valid_castling_destination(self, destination: Position, other_piece: "CastlablePiece") -> bool:
        pass


class Castling(Movement):

    def __init__(self, castlable_piece1: CastlablePiece, castlable_piece2: CastlablePiece):
        move = [MovementData(castlable_piece1, castlable_piece1.position,
                             castlable_piece1.find_castling_destination(castlable_piece2)),
                MovementData(castlable_piece2, castlable_piece2.position,
                             castlable_piece2.find_castling_destination(castlable_piece1))]
        super().__init__(move)

    # def __init__(self, king: King, position: Position):
    #     rooks = king.board.pieces[king.player][Rook]
    #
    #     direction: Position = position - king.position
    #
    #     # Checks if direction is only in one axis
    #     if np.sum(direction != 0) != 1:
    #         raise Exception("Invalid Move")
    #     dir_rooks = np.abs([np.sum(rook.position - position) for rook in rooks])
    #     rook = rooks[np.argmin(dir_rooks)]
    #
    #     if rook.position[~(direction != 0)] != king.position[~(direction != 0)]:
    #         raise Exception("Invalid Axis")
    #
    #     if rook.n_moves or king.n_moves:
    #         raise Exception("King or Rook has already moved once")
    #
    #     # Checks pieces in the path
    #     if any(list(king.board[pos] for pos in king.position.create_lineal_path(rook.position))[:-1]):
    #         raise Exception("Piece in path")
    #
    #     king_pos = king.position.copy_and_replace(direction != 0,
    #                                               (3 if direction.sum() > 0 else 1) * king.board.size // 4)
    #     rook_pos = king_pos + (-(direction != 0).astype(np.int_) if direction.sum() > 0 else (direction != 0))
    #
    #     # Checks during the path of the king
    #     if any(king.board.can_enemy_piece_capture(pos, king.player) for pos in
    #            king.position.create_lineal_path(king_pos)):
    #         raise Exception("King would be in check during path")
    #
    #     move = [MovementData(king, king.position, king_pos), MovementData(rook, rook.position, rook_pos)]
    #     super().__init__(move)

    def check_valid_move(self) -> bool:
        piece1, dest1 = cast(CastlablePiece, self[0].piece), cast(Position, self[0].destination_position)
        piece2, dest2 = cast(CastlablePiece, self[1].piece), cast(Position, self[1].destination_position)
        return piece1.check_valid_castling_destination(dest1, piece2) and \
               piece2.check_valid_castling_destination(dest2, piece1)
