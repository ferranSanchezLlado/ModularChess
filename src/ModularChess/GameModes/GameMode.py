from enum import Enum
from itertools import chain
from typing import Optional, Iterator, Union, cast, Tuple, List

from src.ModularChess.controller.Board import Board
from src.ModularChess.controller.Player import Player
from src.ModularChess.utils.Movement import Movement


class GameState(Enum):
    # TODO
    STARTING = 0
    FINISHED = 1


class GameMode:

    def __init__(self, board: Board, order: Iterator[Player]):
        self.board = board
        self.moves: List[Movement] = []
        self.turn = next(order)
        self.order = order

    def generate_board(self) -> None:
        pass

    def check_game_state(self) -> Tuple[GameState, Optional[Player]]:
        pass

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

        # gen: 1 2 3
        # turn: 3
        # moves: 1 2 3 1 2
        # n_moves: 3

        # player_order: [2, 1, 3] | [3, 1, 2, 3]
        # gen: 3 1 2 3 1 2 3
        for i in range(len(self.moves) - n_moves):
            move = self.moves.pop()
            move.inverse().move()
            player_order.append(move.player)

        if change_turn:
            self.order = chain(reversed(player_order), self.order)
            self.turn = next(self.order)
