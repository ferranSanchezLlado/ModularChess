import abc
from enum import Enum
from itertools import chain
from typing import Iterator, Union, Tuple, List, Type, TYPE_CHECKING

from ModularChess.utils.Movement import Movement

if TYPE_CHECKING:
    from ModularChess.controller.Board import Board
    from ModularChess.controller.Player import Player
    from ModularChess.pieces.Piece import Piece


class GameState(Enum):
    EMPTY = '0'
    STARTING = '1'
    PLAYING = '2'
    FINISHED = '3'
    WIN = '3.1'
    CHECKMATE = '3.1.1'
    DRAW = '3.2'
    STALEMATE = '3.2.1'
    MOVES_50 = '3.2.2'

    def __eq__(self, other) -> bool:
        if not isinstance(other, GameState):
            return False
        self_values = self.value.split('.')
        other_values = other.value.split('.')
        return all(self_digit == other_digit for self_digit, other_digit in zip(self_values, other_values))


class GameMode(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, board: "Board", order: Iterator["Player"], pieces: List[Type["Piece"]]):
        self.board = board
        self.moves: List[Movement] = []
        self.turn = next(order)
        self.order = order
        self.pieces = pieces

        for piece_type in pieces:
            setattr(self, piece_type.__name__, piece_type)

    @abc.abstractmethod
    def generate_board(self) -> None:
        pass

    def generate_moves(self) -> List[Movement]:
        return [move for pieces in list(self.board.pieces[self.turn].values()) for piece in pieces for move in
                piece.get_valid_moves() if self.check_valid_move(move)]

    @abc.abstractmethod
    def check_game_state(self) -> Tuple[GameState, List["Player"]]:
        pass

    @abc.abstractmethod
    def check_valid_move(self, move: Movement) -> bool:
        """Checks if the move is valid in the specific game rules."""
        pass

    def force_move(self, move: Movement) -> None:
        move.move()
        self.moves.append(move)

    def move(self, move: Movement) -> None:
        if move.player != self.turn:
            raise Exception("It's not the players turn")
        if not move.check_valid_move() or not self.check_valid_move(move):
            raise Exception("Invalid Move")

        self.force_move(move)
        self.turn = next(self.order)

    def undo_move(self, move: Union[int, Movement], change_turn=True) -> None:
        if type(move) is int:
            # Number of moves to undo
            n_moves = len(self.moves) - move
            if n_moves < 0 or n_moves > len(self.moves):
                raise Exception("Index Out of Bounds")
        elif isinstance(move, Movement):
            # Until which element should moves be undone
            def search_n_moves() -> int:
                for n, previous_move in enumerate(self.moves):
                    if move is previous_move:
                        return n
                raise Exception("Move not made")

            n_moves = search_n_moves()
        else:
            raise Exception("Unexpected type")

        player_order: List["Player"] = [self.turn]

        for i in range(len(self.moves) - n_moves):
            move = self.moves.pop()
            move.inverse().move()
            player_order.append(move.player)

        if change_turn:
            self.order = chain(reversed(player_order), self.order)
            self.turn = next(self.order)
