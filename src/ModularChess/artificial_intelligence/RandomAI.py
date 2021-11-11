from random import choice
from typing import TYPE_CHECKING, cast

from ModularChess.artificial_intelligence.AI import AI

if TYPE_CHECKING:
    from ModularChess.movements.Movement import Movement


class RandomAI(AI):
    def get_next_move(self) -> "Movement":
        moves = self.evaluator.game_mode.generate_moves()
        return cast("Movement", choice(moves))
