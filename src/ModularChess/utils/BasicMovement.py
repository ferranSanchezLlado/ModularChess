from typing import List, TYPE_CHECKING

from ModularChess.utils.Movement import Movement, MovementData

if TYPE_CHECKING:
    from ModularChess.utils.Position import Position
    from ModularChess.pieces.Piece import Piece


class BasicMovement(Movement):

    def __init__(self, piece: "Piece", new_position: "Position"):
        move: List[MovementData] = []
        # Adds information about capture
        if piece.board.can_capture(piece, new_position):
            enemy_piece = piece.board[new_position]
            assert enemy_piece is not None

            move.append(MovementData(enemy_piece, new_position, None))
        move.append(MovementData(piece, piece.position, new_position))
        super().__init__(move, piece)

    def __str__(self) -> str:
        if self.piece.board.dimensions == 2:
            move = self.piece.abbreviation()
            same_pieces = self.piece.board.pieces[self.player][type(self.piece)]
            if self.movements[-1].destination_position is not None and \
                    len([piece for piece in same_pieces if piece.check_move(self.movements[-1].destination_position)]) \
                    > 1:
                move += str(self.movements[-1].initial_position)
            if len(self) == 2:  # Capture
                move += "x"
            return move + str(self.movements[-1].destination_position) + ("+" if self.is_check else "")
        return super().__str__()
