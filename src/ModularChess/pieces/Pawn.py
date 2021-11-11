import os.path
from abc import ABCMeta
from typing import TextIO

from ModularChess.movements.Promotion import PromotablePiece


class Pawn(PromotablePiece, metaclass=ABCMeta):

    @staticmethod
    def piece_unicode() -> str:
        return "♙"

    @staticmethod
    def abbreviation() -> str:
        return "P"

    @staticmethod
    def image() -> TextIO:
        return open(os.path.join(Pawn.res_path, "Pawn.png"))

    @staticmethod
    def piece_value() -> float:
        return 1
