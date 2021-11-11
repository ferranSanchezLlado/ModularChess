from typing import TYPE_CHECKING, Optional

from ModularChess.movements.Movement import Movement, MovementData

if TYPE_CHECKING:
    from ModularChess.pieces.Piece import Piece
    from ModularChess.utils.Position import Position


class EnPassant(Movement):
    def __init__(self, piece: "Piece", new_position: "Position", captured_piece: "Piece",
                 is_valid_move: Optional[bool] = None):
        moves = [MovementData(captured_piece, captured_piece.position, None),
                 MovementData(piece, piece.position, new_position)]

        super().__init__(moves, piece=piece, destination=new_position, is_valid_move=is_valid_move)

    def __str__(self) -> str:
        if self.piece.board.dimensions == 2:
            move = self.piece.abbreviation()
            same_pieces = self.piece.board.pieces[self.player][type(self.piece)]
            if self.movements[-1].destination_position is not None and \
                    len([piece for piece in same_pieces if
                         piece.check_piece_valid_move(self.movements[-1].destination_position)]) \
                    > 1:
                move += str(self.movements[-1].initial_position)
            if len(self) == 2:  # Capture
                move += "x"
            return move + str(self.movements[-1].destination_position) + ("+" if self.is_check else "")
        return super().__str__()
