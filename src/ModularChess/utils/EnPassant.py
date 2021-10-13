from typing import TYPE_CHECKING

from ModularChess.utils.Movement import Movement, MovementData

if TYPE_CHECKING:
    from ModularChess.pieces.Piece import Piece
    from ModularChess.utils.Position import Position


class EnPassant(Movement):
    def __init__(self, piece: "Piece", new_position: "Position", captured_piece: "Piece"):
        moves = [MovementData(captured_piece, captured_piece.position, None),
                 MovementData(piece, piece.position, new_position)]

        super(EnPassant, self).__init__(moves, piece=piece)
