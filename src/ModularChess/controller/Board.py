from collections import defaultdict
from typing import Type, Optional, cast, Dict, List, TYPE_CHECKING, Tuple, Union

import numpy as np

from ModularChess.pieces.Empty import Empty

if TYPE_CHECKING:
    from ModularChess.controller.Player import Player
    from ModularChess.pieces.Piece import Piece
    from ModularChess.utils.Position import Position


class Board:

    def __init__(self, shape: Tuple[int, ...] = (8, 8)):

        if len(shape) < 2:
            raise Exception("Board should at least have 2 dimensions")

        # Maybe sparse
        self.board = np.empty(shape, dtype=object)

        self.pieces: Dict["Player", Dict[Type["Piece"], List["Piece"]]] = defaultdict(lambda: defaultdict(list))

    def __getitem__(self, position: Union["Position", Tuple[int, ...]]) -> Optional["Piece"]:
        # Already checked during access
        # if self.is_position_outside(position):
        #     raise Exception("position out of board")

        try:
            piece = cast(Optional["Piece"], self.board[tuple(position)])
        except Exception:
            raise Exception("position out of board")

        return piece

    def __setitem__(self, position: Union["Position", Tuple[int, ...]], piece: Optional["Piece"]) -> None:
        try:
            self.board[tuple(position)] = piece
        except Exception:
            raise Exception("position out of board")

    def __str__(self) -> str:
        # Flips all axis excluding y, making the point 0 to be the lower left corner
        return str(np.flip(self.board, axis=[i for i in range(self.dimensions) if i != 1])).replace("None", "□")

    def __repr__(self) -> str:
        return repr(self.board) + "|" + repr(self.pieces)

    @property
    def dimensions(self):
        return self.board.ndim

    @property
    def size(self):
        shape = self.shape
        if any(i != shape[0] for i in shape):
            return -1  # Maybe max
        return shape[0]

    @property
    def shape(self) -> Tuple[int, ...]:
        return cast(Tuple[int, ...], self.board.shape)

    def add_piece(self, piece: "Piece") -> None:
        self[piece.position] = piece

        self.pieces[piece.player][type(piece)].append(piece)

    def remove_piece(self, piece: "Piece") -> None:
        self[piece.position] = None

        self.pieces[piece.player][type(piece)].remove(piece)

    def move_piece(self, piece: "Piece", new_position: "Position"):
        self[piece.position] = None
        self[new_position] = piece

        piece.n_moves += 1
        piece.position = new_position

    def can_enemy_piece_capture_piece(self, piece: "Piece") -> Optional["Piece"]:
        for enemy_player in piece.player.enemies:
            for enemy_pieces in self.pieces[enemy_player].values():
                for enemy_piece in enemy_pieces:
                    if enemy_piece.check_move(piece.position):
                        return piece
        return None

    def can_enemy_piece_capture_position(self, position: "Position", player: "Player") -> Optional["Piece"]:
        previous_piece = self[position]
        if previous_piece is not None:
            self.remove_piece(previous_piece)
        temporal_piece = Empty(self, player, position)
        self.add_piece(temporal_piece)

        result = self.can_enemy_piece_capture_piece(temporal_piece)

        self.remove_piece(temporal_piece)
        if previous_piece is not None:
            self.add_piece(previous_piece)
        return result

    def can_capture_or_move(self, piece: "Piece", new_position: "Position") -> bool:
        destination = self[new_position]
        return destination is None or piece.player.can_capture(destination.player)

    def can_capture(self, piece: "Piece", new_position: "Position") -> bool:
        destination = self[new_position]
        return destination is not None and piece.player.can_capture(destination.player)

    def is_position_outside(self, position: "Position") -> bool:
        return position.shape[0] == self.dimensions and np.any(
            (position < 0) | (position >= self.shape))  # type: ignore

    def is_position_inside(self, position: "Position") -> bool:
        return position.shape[0] == self.dimensions and np.all(
            (position >= 0) & (position < self.shape))  # type: ignore

    def to_generic_fen(self) -> str:
        # Piece + Player index
        # end line as level separator
        pass

    @classmethod
    def from_fen(cls, fen: str) -> "Board":
        pass
