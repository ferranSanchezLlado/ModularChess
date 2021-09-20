from dataclasses import dataclass
from typing import Optional, List

from src.ModularChess.controller.Player import Player
from src.ModularChess.pieces.Piece import Piece
from src.ModularChess.utils.Position import Position


@dataclass
class MovementData:
    piece: Piece
    initial_position: Optional[Position]
    destination_position: Optional[Position]

    def __iter__(self):
        return iter((self.piece, self.initial_position, self.destination_position))


class Movement:

    def __init__(self, movements: List[MovementData], player: Optional[Player] = None):
        self.movements = movements
        self.player: Player = player or movements[0].piece.player

    def __getitem__(self, index: int) -> MovementData:
        return self.movements[index]

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
            def move(self) -> None:
                super().move()
                for piece, initial_position, destination_position in self.movements:
                    if initial_position is not None and destination_position is not None:
                        piece.n_moves -= 2  # Cancels Previous two moves

        return InverseMovement([MovementData(move.piece, move.destination_position, move.initial_position) for move in
                                reversed(self.movements)])
