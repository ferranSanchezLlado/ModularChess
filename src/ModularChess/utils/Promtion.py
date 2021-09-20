from typing import Type

from src.ModularChess.pieces.Piece import Piece
from src.ModularChess.utils.Movement import Movement, MovementData
from src.ModularChess.utils.Position import Position


class Promotion(Movement):

    def __init__(self, piece: Piece, new_position: Position, promotion_piece: Type[Piece]):
        promoted_piece = promotion_piece(piece.board, piece.player, new_position)
        promoted_piece.n_moves = piece.n_moves + 1

        super().__init__([MovementData(piece, piece.position, None),
                          MovementData(promoted_piece, None, promoted_piece.position)])

    def check_valid_move(self) -> bool:
        return super().check_valid_move()
