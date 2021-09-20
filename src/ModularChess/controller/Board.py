from __future__ import annotations

from typing import Type, Optional, cast, Dict, List

import numpy as np

from src.ModularChess.pieces.Piece import Piece
from src.ModularChess.controller.Player import Player
from src.ModularChess.utils.Position import Position


class Board:

    def __init__(self, size=8, dimensions=2):
        # Sparse matrix + map piece position
        self.size = size
        self.dimensions = dimensions

        # Maybe sparse
        self.board = np.empty([size] * dimensions, dtype=object)

        self.pieces: Dict[Player, Dict[Type[Piece], List[Piece]]] = {}

    def __getitem__(self, position: Position) -> Optional[Piece]:
        if self.is_position_outside(position):
            raise Exception("position out of board")

        piece = cast(Optional[Piece], self.board[tuple(position)])
        return piece

    def __str__(self) -> str:
        # Flips all axis excluding y, making the point 0 to be the lower left corner
        return str(np.flip(self.board, axis=[i for i in range(self.dimensions) if i != 1]))

    def add_piece(self, piece: Piece) -> None:
        self.board[tuple(piece.position)] = piece

        self.pieces.setdefault(piece.player, {})
        self.pieces[piece.player].setdefault(piece.__class__, [])
        self.pieces[piece.player][piece.__class__].append(piece)

    def remove_piece(self, piece: Piece) -> None:
        self.board[tuple(piece.position)] = None

        self.pieces[piece.player][piece.__class__].remove(piece)

    def move_piece(self, piece: Piece, new_position: Position):
        self.board[tuple(piece.position)] = None
        self.board[tuple(new_position)] = piece

        piece.n_moves += 1
        piece.position = new_position

    def can_enemy_capture(self, position: Position, allied_players: list[Player]) -> bool:
        for player in list(player for player in self.pieces.keys() if player not in allied_players):
            for pieces in self.pieces[player].values():
                for piece in pieces:
                    if piece.check_move(position):
                        return True
        return False

    def can_capture_or_move(self, piece: Piece, new_position: Position) -> bool:
        enemy_players = list(player for player in self.pieces.keys() if player not in piece.player.get_allies())
        destination = self[new_position]
        # TODO: use player method
        return destination is None or destination.player in enemy_players

    def is_there_an_enemy_piece(self, piece: Piece, new_position: Position) -> bool:
        enemy_players = list(player for player in self.pieces.keys() if player not in piece.player.get_allies())
        destination = self[new_position]
        return destination is not None and destination.player in enemy_players

    def is_position_outside(self, position: Position) -> bool:
        return bool(np.any((position < 0) | (position >= self.size))) and position.shape[0] == self.dimensions

    def is_position_inside(self, position: Position) -> bool:
        return bool(np.any((position >= 0) | (position < self.size))) and position.shape[0] == self.dimensions
