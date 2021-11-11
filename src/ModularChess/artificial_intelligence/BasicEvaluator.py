from typing import TYPE_CHECKING

from ModularChess.artificial_intelligence.Evaluator import Evaluator

if TYPE_CHECKING:
    from ModularChess.controller.Player import Player
    from ModularChess.game_modes.GameMode import GameMode


class BasicEvaluator(Evaluator):

    def __init__(self, game_mode: "GameMode"):
        super().__init__(game_mode)

    def evaluate_player(self, player: "Player") -> float:
        # Check if the player is in checkmate
        return sum(piece.piece_value() for pieces in self.game_mode.board.pieces[player].values() for piece in pieces)
