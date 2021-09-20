from src.ModularChess.pieces.Piece import Piece


class Empty(Piece):

    def __repr__(self) -> str:
        return "□"
