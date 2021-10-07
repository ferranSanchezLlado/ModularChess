from typing import List, TYPE_CHECKING

from ModularChess.pieces.Bishop import Bishop
from ModularChess.pieces.Piece import Piece
from ModularChess.pieces.Rook import Rook

if TYPE_CHECKING:
    from ModularChess.utils.Movement import Movement
    from ModularChess.utils.Position import Position


class Queen(Piece):

    def check_move(self, new_position: "Position") -> List["Movement"]:
        # Piece didn't move or outside board
        if super().check_move(new_position) is None:
            return []
        return Bishop.two_lineal_check_move(self, new_position) or Rook.lineal_check_move(self, new_position)

    def get_valid_moves(self) -> List["Movement"]:
        return Bishop.get_bishop_valid_moves(self) + Rook.get_rook_valid_moves(self)

    def __repr__(self) -> str:
        return "♕"

    def abbreviation(self) -> str:
        return "Q"
