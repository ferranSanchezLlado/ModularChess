import abc
from typing import TYPE_CHECKING, Tuple, List, Optional

if TYPE_CHECKING:
    from ModularChess.controller.Player import Player
    from ModularChess.game_modes.GameMode import GameMode


class Evaluator(metaclass=abc.ABCMeta):
    def __init__(self, game_mode: "GameMode"):
        self.game_mode = game_mode

    @abc.abstractmethod
    def evaluate_player(self, player: "Player") -> float:
        pass

    def evaluate(self) -> List[Tuple["Player", float]]:
        return [(player, self.evaluate_player(player)) for player in self.game_mode.players]

    def score(self, player: Optional["Player"] = None) -> float:
        player_to_score: "Player" = self.game_mode.current_player_turn if player is None else player
        player_score = self.evaluate_player(player_to_score)

        n_allies = len(player_to_score.allies) - 1
        allies_score = sum(self.evaluate_player(pl) for pl in player_to_score.allies if pl != player_to_score)

        n_enemies = len(player_to_score.enemies)
        enemy_score = sum(self.evaluate_player(pl) for pl in player_to_score.enemies)

        if not n_allies:
            return player_score - enemy_score / n_enemies

        player_coefficient = 0.75
        allies_coefficient = 1 - player_coefficient
        return (player_coefficient * player_score +
                allies_coefficient * allies_score / n_allies) - enemy_score / n_enemies
