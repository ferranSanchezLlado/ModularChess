from abc import ABCMeta

from ModularChess.utils.Promotion import PromotablePiece


class Pawn(PromotablePiece, metaclass=ABCMeta):

    def __repr__(self) -> str:
        return "♙"
