import abc
from enum import Enum
from itertools import chain
from typing import Optional, Iterator, Union, cast, Tuple, List, Type

from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.pieces.Piece import Piece
from ModularChess.utils.Movement import Movement


class GameState(Enum):
    # TODO
    STARTING = 0
    FINISHED = 1


class GameMode(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, board: Board, order: Iterator[Player], pieces: List[Type[Piece]]):
        self.board = board
        self.moves: List[Movement] = []
        self.turn = next(order)
        self.order = order
        self.pieces = pieces

    @abc.abstractmethod
    def generate_board(self) -> None:
        pass

    @abc.abstractmethod
    def check_game_state(self) -> Tuple[GameState, Optional[Player]]:
        pass

    @abc.abstractmethod
    def check_valid_move(self, move: Movement) -> bool:
        """Checks if the move is valid in the specific game rules."""
        pass

    def force_move(self, move: Movement) -> None:
        move.move()
        self.moves.append(move)

    def move(self, move: Movement) -> None:
        if not move.check_valid_move() or not self.check_valid_move(move):
            raise Exception("Invalid Move")
        if move[0].piece.player is not self.turn:
            raise Exception("It's not the players turn")
        self.force_move(move)
        self.turn = next(self.order)

    def undo_move(self, move: Union[int, Movement], change_turn=True) -> None:
        if type(move) is int:
            # Number of moves to undo
            n_moves = len(self.moves) - move
            if n_moves < 0 or n_moves > len(self.moves):
                raise Exception("Index Out of Bounds")
        elif issubclass(type(move), Movement):
            try:
                # Until which element should moves be undone
                n_moves = self.moves.index(cast(Movement, move))
            except ValueError:
                raise Exception("Move not made")
        else:
            raise Exception("Unexpected type")

        player_order: List[Player] = [self.turn]

        for i in range(len(self.moves) - n_moves):
            move = self.moves.pop()
            move.inverse().move()
            player_order.append(move.player)

        if change_turn:
            self.order = chain(reversed(player_order), self.order)
            self.turn = next(self.order)
