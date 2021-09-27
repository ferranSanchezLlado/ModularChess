from typing import List

from ModularChess.pieces.Piece import Piece
from ModularChess.utils.Movement import Movement, MovementData
from ModularChess.utils.Position import Position


class BasicMovement(Movement):

    def __init__(self, piece: Piece, new_position: Position):
        move: List[MovementData] = []
        # Adds information about capture
        if piece.board.is_an_enemy_piece(piece, new_position):
            enemy_piece = piece.board[new_position]
            assert enemy_piece is not None

            move.append(MovementData(enemy_piece, new_position, None))
        move.append(MovementData(piece, piece.position, new_position))
        super().__init__(move)

    def check_valid_move(self) -> bool:
        return super().check_valid_move()
