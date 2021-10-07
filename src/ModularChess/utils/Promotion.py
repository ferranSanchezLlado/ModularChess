import abc
from typing import Type, List, TYPE_CHECKING

from ModularChess.pieces.Piece import Piece
from ModularChess.utils.Movement import Movement, MovementData

if TYPE_CHECKING:
    from ModularChess.utils.Position import Position
    from ModularChess.controller.Board import Board
    from ModularChess.controller.Player import Player


class PromotablePiece(Piece, metaclass=abc.ABCMeta):
    # TODO

    @abc.abstractmethod
    def __init__(self, board: "Board", player: "Player", starting_position: "Position",
                 valid_pieces_type: List[Type["Piece"]]):
        super().__init__(board, player, starting_position)
        self.valid_pieces_type = valid_pieces_type

    @abc.abstractmethod
    def can_promote_in_position(self, new_position: "Position") -> bool:
        """Checks if the piece can promote at the new_position.

        :param new_position: position to check promotion
        :return: True if the piece can promote
        """
        pass

    def is_a_valid_piece_to_promote(self, piece: "Piece") -> bool:
        return type(piece) in self.valid_pieces_type


class Promotion(Movement):

    def __init__(self, piece: "PromotablePiece", new_position: "Position", promotion_piece_type: Type["Piece"]):
        promoted_piece = promotion_piece_type(piece.board, piece.player, new_position)
        promoted_piece.n_moves = piece.n_moves + 1
        self.promotable_piece = piece

        move: List[MovementData] = []
        if piece.board.can_capture(piece, new_position):
            enemy_piece = piece.board[new_position]
            assert enemy_piece is not None

            move.append(MovementData(enemy_piece, new_position, None))
        move.append(MovementData(piece, piece.position, None))
        move.append(MovementData(promoted_piece, None, promoted_piece.position))
        super().__init__(move, piece)

    def check_valid_move(self) -> bool:
        destination_promoted_piece = self[-1].destination_position
        assert destination_promoted_piece is not None
        return self.promotable_piece.can_promote_in_position(destination_promoted_piece) and \
            self.promotable_piece.is_a_valid_piece_to_promote(self[-1].piece) and super().check_valid_move()
