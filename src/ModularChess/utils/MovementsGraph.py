import dataclasses
from typing import List, TYPE_CHECKING, Optional, cast

if TYPE_CHECKING:
    from ModularChess.utils.Movement import Movement


@dataclasses.dataclass
class MovementsNode:
    parent: Optional["MovementsNode"]
    move: "Movement"
    children: List["MovementsNode"] = dataclasses.field(default_factory=list)

    def __len__(self) -> int:
        return len(self.children)

    def find_children_move(self, move: "Movement") -> Optional["MovementsNode"]:
        for node in self.children:
            if node.move == move:
                return node
        return None


@dataclasses.dataclass
class MovementsGraph:
    root: Optional[MovementsNode] = None
    current: Optional[MovementsNode] = None
    direction_right: bool = True
    n_moves: int = 0

    def __iter__(self) -> "MovementsGraph":
        return self

    def __next__(self) -> MovementsNode:
        if self.current is None:
            raise StopIteration
        if self.direction_right:
            if len(self.current) == 0:
                raise StopIteration
            self.current = self.current.children[0]
        else:
            if self.current.parent is None:
                raise StopIteration
            self.current = self.current.parent
        return self.current

    def next(self, move: "Movement") -> MovementsNode:
        if self.current is None:
            raise StopIteration
        child = self.current.find_children_move(move)
        if child is None:
            raise StopIteration
        self.current = child
        return child

    def add(self, move: "Movement") -> MovementsNode:
        child: MovementsNode
        if self.current is None:
            child = MovementsNode(None, move)
            self.root = self.current = child
        else:
            search_child = self.current.find_children_move(move)
            if search_child is None:
                child = MovementsNode(self.current, move)
                self.current.children.append(child)
                self.n_moves += 1
            else:
                child = search_child
        return child

    def add_and_next(self, move: "Movement") -> MovementsNode:
        self.current = self.add(move)
        return self.current

    def remove(self) -> None:
        if self.root == self.current:
            if self.root is None:
                raise Exception()
            self.root = self.current = None
        current = cast(MovementsNode, self.current)
        self.current = current.parent
        assert self.current is not None
        del self.current.children[self.current.children.index(current)]
        self.n_moves -= 1 + len(current)

    def get_moves(self) -> List["Movement"]:
        direction = self.direction_right
        self.direction_right = False
        moves = [move_data.move for move_data in self]
        self.direction_right = direction
        return moves[::-1]

    def __reversed__(self) -> "MovementsGraph":
        self.direction_right = not self.direction_right
        return self
