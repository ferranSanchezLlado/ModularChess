import os.path
from abc import ABCMeta
from typing import TextIO

from ModularChess.utils.Promotion import PromotablePiece


class Pawn(PromotablePiece, metaclass=ABCMeta):

    @staticmethod
    def piece_unicode() -> str:
        return "♙"

    @staticmethod
    def abbreviation() -> str:
        return ""

    @staticmethod
    def image() -> TextIO:
        return open(os.path.join(Pawn.res_path, "Pawn.png"))
