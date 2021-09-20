from typing import List

from src.ModularChess.pieces.Bishop import Bishop
from src.ModularChess.pieces.Piece import Piece
from src.ModularChess.pieces.Rook import Rook
from src.ModularChess.utils.Movement import Movement
from src.ModularChess.utils.Position import Position


class Queen(Piece):

    def check_move(self, new_position: Position) -> bool:
        # Piece didn't move or outside board
        if not super().check_move(new_position):
            return False
        return Bishop.two_lineal_check_move(self, new_position) or Rook.lineal_check_move(self, new_position)

    # noinspection PyTypeChecker
    def get_valid_moves(self) -> List[Movement]:
        return Bishop.get_bishop_valid_moves(self) + Rook.get_rook_valid_moves(self)

    def __repr__(self) -> str:
        return "♕"
