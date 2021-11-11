import abc
from collections import deque
from enum import Enum
from itertools import chain
from typing import Iterator, Union, Tuple, List, Type, TYPE_CHECKING, Hashable, Callable, TypeVar, Optional

from ModularChess.movements.Movement import Movement
from ModularChess.utils.Exceptions import InvalidMoveException, InvalidArgumentsError

if TYPE_CHECKING:
    from ModularChess.controller.Board import Board
    from ModularChess.controller.Player import Player
    from ModularChess.pieces.Piece import Piece

RT = TypeVar('RT')  # return type


def cache_game_mode(arg: Union[Callable[..., RT], int]):
    cache_deque: deque[Tuple[int, RT]]
    if callable(arg) or arg is None:
        cache_deque = deque(maxlen=5)
    elif type(arg) is int:
        cache_deque = deque(maxlen=arg)
    else:
        raise InvalidArgumentsError("Decorator argument must be an integer or empty")

    def find_result(key_to_find: int) -> Optional[RT]:
        return next((element for index, (key, element) in enumerate(cache_deque) if key_to_find == key), None)

    def cache_decorator(func: Callable[..., RT]):
        def cache(self: Hashable, *args, **kwargs) -> RT:
            hash_self = hash(self)
            result = find_result(hash_self)
            if result is None:
                result = func(self, *args, **kwargs)
                cache_deque.append((hash_self, result))
            return result

        return cache

    if callable(arg):
        return cache_decorator(arg)
    else:
        return cache_decorator


class GameState(Enum):
    EMPTY_BOARD = '0'
    STARTING = '1'
    PLAYING = '2'
    FINISHED = '3'
    WIN = '3.1'
    CHECKMATE = '3.1.1'
    DRAW = '3.2'
    STALEMATE = '3.2.1'
    MOVES_50 = '3.2.2'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Enum) and other not in GameState:
            return False
        self_levels = self.value.split('.')
        other_levels = other.value.split('.')
        return all(self_level == other_level for self_level, other_level in zip(self_levels, other_levels))


class GameMode(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, board: "Board", order: Iterator["Player"], players: List["Player"], pieces: List[Type["Piece"]]):
        self.board = board
        self.moves: List[Movement] = []
        self.current_player_turn = next(order)
        self.order = order
        self.players = players
        self.pieces = pieces

        for piece_type in pieces:
            setattr(self, piece_type.__name__, piece_type)

    @abc.abstractmethod
    def generate_board(self) -> None:
        pass

    @cache_game_mode(400)
    def generate_moves(self) -> List[Movement]:
        return [move for pieces in list(self.board.pieces[self.current_player_turn].values()) for piece in pieces for
                move in
                piece.get_piece_valid_moves() if self.check_valid_move(move)]

    def generate_moves_of_a_piece(self, piece: "Piece") -> List[Movement]:
        return [move for move in piece.get_piece_valid_moves() if self.check_valid_move(move)]

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
        if move.player != self.current_player_turn:
            raise InvalidMoveException("It's not the players turn")
        if not move.check_valid_move():
            raise InvalidMoveException("Invalid piece move")
        if not self.check_valid_move(move):
            raise InvalidMoveException("Move doesn't follow the game mode rules")

        self.force_move(move)
        self.current_player_turn = next(self.order)

    def undo_move(self, move: Union[int, Movement], change_turn=True) -> None:
        if type(move) is int:
            # Number of moves to undo
            n_moves = len(self.moves) - move
            if n_moves < 0 or n_moves > len(self.moves):
                raise InvalidMoveException("Index Out of Bounds")
        elif isinstance(move, Movement):
            # Until which element should moves be undone
            def search_n_moves() -> int:
                for n, previous_move in enumerate(self.moves):
                    if move is previous_move:
                        return n
                raise InvalidMoveException("Move wasn't made")

            n_moves = search_n_moves()
        else:
            raise InvalidArgumentsError("Unexpected type")

        player_order: List["Player"] = [self.current_player_turn]

        for i in range(len(self.moves) - n_moves):
            move = self.moves.pop()
            move.inverse().move()
            player_order.append(move.player)

        if change_turn:
            self.order = chain(reversed(player_order), self.order)
            self.current_player_turn = next(self.order)

    @abc.abstractmethod
    def restart(self) -> None:
        pass

    def __hash__(self):
        return hash(tuple(self.moves))

    @abc.abstractmethod
    def to_fen(self) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def from_fen(cls, fen: str) -> "GameMode":
        pass
