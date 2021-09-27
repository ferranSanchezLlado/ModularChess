import abc
from dataclasses import dataclass
from typing import Optional, List, Any, no_type_check

import numpy as np

from ModularChess.controller.Player import Player
from ModularChess.pieces.Piece import Piece
from ModularChess.utils.Position import Position


@dataclass
class MovementData:
    piece: Piece
    initial_position: Optional[Position]
    destination_position: Optional[Position]

    def __iter__(self):
        return iter((self.piece, self.initial_position, self.destination_position))

    @no_type_check
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, MovementData) and self.piece == other.piece and \
               np.array_equal(self.initial_position, other.initial_position) and \
               np.array_equal(self.destination_position, other.destination_position)


class Movement(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, movements: List[MovementData], player: Optional[Player] = None):
        self.movements = movements
        self.player: Player = player or movements[0].piece.player

    def __getitem__(self, index: int) -> MovementData:
        return self.movements[index]

    def __len__(self) -> int:
        return len(self.movements)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Movement) and len(self) == len(other) and self.player == other.player and \
               all(move1 == move2 for move1, move2 in zip(self.movements, other.movements))

    def move(self) -> None:
        for piece, initial_position, destination_position in self.movements:
            if initial_position is None:
                piece.board.add_piece(piece)
            elif destination_position is None:
                piece.board.remove_piece(piece)
            else:
                piece.board.move_piece(piece, destination_position)

    def check_valid_move(self) -> bool:
        position = self.movements[0].destination_position
        return position is None or self.movements[0].piece.check_move(position)

    def inverse(self) -> "Movement":
        class InverseMovement(Movement):
            def __init__(self, move: Movement):
                super(InverseMovement, self).__init__([MovementData(
                    move.piece, move.destination_position, move.initial_position) for move in reversed(move.movements)],
                    player=move.player)

            def move(self) -> None:
                super().move()
                for piece, initial_position, destination_position in self.movements:
                    if initial_position is not None and destination_position is not None:
                        piece.n_moves -= 2  # Reduces number of moves (if piece has moved)

        return InverseMovement(self)
