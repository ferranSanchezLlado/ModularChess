import abc
from typing import Type, List, cast, Optional, TYPE_CHECKING

import numpy as np

from ModularChess.movements.Movement import Movement, MovementData
from ModularChess.pieces.Piece import Piece
from ModularChess.utils.Exceptions import InvalidMoveException

if TYPE_CHECKING:
    from ModularChess.controller.Board import Board
    from ModularChess.controller.Player import Player
    from ModularChess.utils.Position import Position


class CastlablePiece(Piece, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, board: "Board", player: "Player", starting_position: "Position",
                 castlable_pieces: Optional[List[Type["CastlablePiece"]]] = None):
        super().__init__(board, player, starting_position)
        self.castlable_pieces: List[Type["CastlablePiece"]] = castlable_pieces or [
            piece_type for piece_type in board.pieces[player].keys() if issubclass(piece_type, CastlablePiece)]

    def get_possible_castlable_pieces(self) -> List["CastlablePiece"]:
        return [cast(CastlablePiece, piece) for piece_type in self.castlable_pieces for piece in
                self.board.pieces[self.player].get(piece_type, []) if piece.n_moves == 0]

    def find_nearest_piece(self, aprox_direction: "Position") -> "CastlablePiece":
        possible_castlable_pieces = self.get_possible_castlable_pieces()

        if len(possible_castlable_pieces) == 0:
            raise InvalidMoveException("No Pieces To Castle")

        direction: Position = aprox_direction - self.position

        # Checks if direction is only in one axis
        if np.sum(direction != 0) != 1:
            raise InvalidMoveException("Invalid Move")
        dir_pieces = np.abs([np.sum(piece.position - aprox_direction) for piece in possible_castlable_pieces])
        nearest_piece: CastlablePiece = possible_castlable_pieces[np.argmin(dir_pieces)]

        # Checks piece is in same axis as direction
        if np.any((nearest_piece.position - self.position)[direction == 0]):  # type: ignore
            raise InvalidMoveException("Invalid Move")

        return nearest_piece

    @abc.abstractmethod
    def find_castling_destination(self, other_piece: "CastlablePiece") -> "Position":
        pass

    @abc.abstractmethod
    def check_valid_castling_destination(self, destination: "Position", other_piece: "CastlablePiece") -> bool:
        pass


class Castling(Movement):

    def __init__(self, castlable_piece1: CastlablePiece, castlable_piece2: CastlablePiece,
                 is_valid_move: Optional[bool] = None):
        move = [MovementData(castlable_piece1, castlable_piece1.position,
                             castlable_piece1.find_castling_destination(castlable_piece2)),
                MovementData(castlable_piece2, castlable_piece2.position,
                             castlable_piece2.find_castling_destination(castlable_piece1))]
        super().__init__(move, castlable_piece1, castlable_piece2.position, is_valid_move=is_valid_move)

    def _check_valid_move(self) -> bool:
        piece1, dest1 = cast(CastlablePiece, self[0].piece), cast("Position", self[0].destination_position)
        piece2, dest2 = cast(CastlablePiece, self[1].piece), cast("Position", self[1].destination_position)
        return piece1.check_valid_castling_destination(dest1, piece2) and (
            piece2.check_valid_castling_destination(dest2, piece1))
