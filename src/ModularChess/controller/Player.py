from dataclasses import dataclass, field
from typing import Optional, Tuple, List


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
        return self != other or not (self.team is not None and other in self.team)

    def get_allies(self) -> "List[Player]":
        return [self] + self.team
