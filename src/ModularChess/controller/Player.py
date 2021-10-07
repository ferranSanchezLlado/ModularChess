from dataclasses import dataclass, field
from typing import Tuple, List


@dataclass
class Player:
    name: str
    color: Tuple[int, int, int] = field(default=(-1, -1, -1))
    allies: List["Player"] = field(default_factory=list)
    enemies: List["Player"] = field(default_factory=list)

    def __post_init__(self):
        self.allies = self.allies or [self]

    def __repr__(self) -> str:
        return self.name

    def __hash__(self):
        return hash(self.name) + hash(self.color)

    def can_capture(self, other: "Player"):
        # Checks enemies, in case enemies is empty, will treat all other players excluding allies as enemies
        return self != other and ((len(self.enemies) == 0 and other not in self.allies) or (other in self.enemies))

    @classmethod
    def join_allies(cls, allies: List["Player"], all_player: List["Player"]) -> None:
        for player in allies:
            player.allies = allies.copy()
            player.enemies = [enemy_player for enemy_player in all_player if enemy_player not in allies]
