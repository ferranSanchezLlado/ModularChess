import abc
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Any, no_type_check, TYPE_CHECKING, cast

import numpy as np

from ModularChess.utils.Exceptions import InvalidArgumentsError

if TYPE_CHECKING:
    from ModularChess.pieces.Piece import Piece
    from ModularChess.utils.Position import Position


class MovementType(Enum):
    UPDATE = 1
    ADDITION = 2
    REMOVAL = 3


@dataclass
class MovementData:
    piece: "Piece"
    initial_position: Optional["Position"]
    destination_position: Optional["Position"]

    def __post_init__(self):
        if self.initial_position is None and self.destination_position is None:
            raise InvalidArgumentsError("Invalid Movement. This movement does not change anything")

    def __iter__(self):
        return iter((self.piece, self.initial_position, self.destination_position))

    def __hash__(self):
        return hash((self.piece, self.initial_position if self.initial_position is not None else 0,
                     self.destination_position if self.destination_position is not None else 0))

    @no_type_check
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, MovementData) and self.piece == other.piece and \
               np.array_equal(self.initial_position, other.initial_position) and \
               np.array_equal(self.destination_position, other.destination_position)

    def __str__(self) -> str:
        return str(self.piece) + ": " + str(self.initial_position) + " -> " + str(self.destination_position)

    @property
    def type(self) -> MovementType:
        if self.initial_position is None:
            return MovementType.ADDITION
        elif self.destination_position is None:
            return MovementType.REMOVAL
        return MovementType.UPDATE


class Movement(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, movements: List[MovementData], piece: Optional["Piece"] = None,
                 destination: Optional["Position"] = None, is_valid_move: Optional[bool] = None):
        self.movements = tuple(movements)
        self.piece: "Piece" = piece or movements[-1].piece
        self.destination: "Position" = destination if destination is not None else \
            cast("Position", movements[-1].destination_position)

        self.is_check = False
        self._is_valid_move = is_valid_move

    @property
    def player(self):
        return self.piece.player

    def __getitem__(self, index: int) -> MovementData:
        return self.movements[index]

    def __len__(self) -> int:
        return len(self.movements)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Movement) and len(self) == len(other) and self.player == other.player and \
               all(move1 == move2 for move1, move2 in zip(self.movements, other.movements))

    def __str__(self) -> str:
        # TODO
        # Piece + origin + (capture) + destination + (promotion piece)
        # Castling: O-O or O-O-O
        # 1: capture (optional)
        # 2: piece
        # 3: promotion (optional) =Q
        return '[' + ', '.join(str(move) for move in self.movements) + ']'

    def __repr__(self) -> str:
        return repr(self.movements)

    def __hash__(self):
        return hash(self.movements)

    def move(self) -> None:
        for move in self.movements:
            move_type = move.type
            if move_type == MovementType.ADDITION:
                assert move.destination_position is not None
                move.piece.position = move.destination_position
                move.piece.board.add_piece(move.piece)
            elif move_type == MovementType.REMOVAL:
                # TODO: Negative position or None
                move.piece.board.remove_piece(move.piece)
            else:
                assert move.destination_position is not None
                move.piece.board.move_piece(move.piece, move.destination_position)

        # TODO: SAVE FEM, allowing reconstruction of board
        self.is_check = False  # self._will_be_check()

    def _check_valid_move(self) -> bool:
        return self in self.piece.check_piece_valid_move(self.destination)

    def check_valid_move(self) -> bool:
        if self._is_valid_move is None:
            self._is_valid_move = self._check_valid_move()
        return self._is_valid_move

    def piece_is_captured(self) -> bool:
        return any(self.player.can_capture(move.piece.player) for move in self.movements)

    def captured_pieces(self) -> List["Piece"]:
        return [move.piece for move in self.movements if move.type == MovementType.REMOVAL and
                self.player.can_capture(move.piece.player)]

    def _will_be_check(self) -> bool:
        from ModularChess.pieces.King import King

        return any(King in self.piece.board.pieces[enemy] and self.piece.board.can_enemy_piece_capture_piece(
            self.piece.board.pieces[enemy][King][0]) for enemy in self.player.enemies)

    def inverse(self) -> "Movement":
        return InverseMovement(self)


class InverseMovement(Movement):
    def __init__(self, move: Movement):
        super().__init__([MovementData(move.piece, move.destination_position, move.initial_position)
                          for move in reversed(move.movements)], piece=move.piece)

    def move(self) -> None:
        super().move()
        for piece, initial_position, destination_position in self.movements:
            if initial_position is not None and destination_position is not None:
                piece.n_moves -= 2  # Reduces number of moves (if piece has moved)
