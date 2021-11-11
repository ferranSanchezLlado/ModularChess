import os
from typing import List, TYPE_CHECKING, TextIO

from ModularChess.pieces.Bishop import Bishop
from ModularChess.pieces.Piece import Piece
from ModularChess.pieces.Rook import Rook

if TYPE_CHECKING:
    from ModularChess.movements.Movement import Movement
    from ModularChess.utils.Position import Position


class Queen(Piece):

    def check_piece_valid_move(self, new_position: "Position") -> List["Movement"]:
        # Piece didn't move or outside board
        if super().check_piece_valid_move(new_position) is None:
            return []
        return Bishop.two_lineal_check_move(self, new_position) or Rook.lineal_check_move(self, new_position)

    def get_piece_valid_moves(self) -> List["Movement"]:
        return Bishop.get_bishop_valid_moves(self) + Rook.get_rook_valid_moves(self)

    @staticmethod
    def piece_unicode() -> str:
        return "♕"

    @staticmethod
    def abbreviation() -> str:
        return "Q"

    @staticmethod
    def image() -> TextIO:
        return open(os.path.join(Queen.res_path, "Queen.png"))

    @staticmethod
    def piece_value() -> float:
        return 9
