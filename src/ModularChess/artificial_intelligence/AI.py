import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ModularChess.movements.Movement import Movement
    from ModularChess.artificial_intelligence.Evaluator import Evaluator
    from ModularChess.controller.Player import Player


class AI(metaclass=abc.ABCMeta):

    def __init__(self, player: "Player", evaluator: "Evaluator"):
        self.player = player
        self.evaluator = evaluator

    @abc.abstractmethod
    def get_next_move(self) -> "Movement":
        pass

    def play_next_move(self) -> None:
        self.evaluator.game_mode.move(self.get_next_move())
