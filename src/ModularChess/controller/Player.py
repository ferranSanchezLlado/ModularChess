from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Iterable


@dataclass
class Player:
    name: str
    color: Optional[Tuple[int, int, int]] = field(default=None)
    team: "List[Player]" = field(default_factory=list)

    def __repr__(self) -> str:
        return self.name

    def __hash__(self):
        return hash(self.name)

    def can_capture(self, other: "Player"):
        return self != other and not (self.team is not None and other in self.team)

    def get_allies(self) -> "List[Player]":
        return [self] + self.team

    def get_enemies(self, all_players: "Iterable[Player]") -> "List[Player]":
        # TODO: save
        allies = set(self.get_allies())
        return list(player for player in all_players if player not in allies)

    @classmethod
    def join_allies(cls, allies: "List[Player]") -> None:
        for player in allies:
            # TODO: Maybe upgrade allies to self-reference
            allies_without_player = allies.copy()
            allies_without_player.remove(player)
            player.team = allies_without_player
