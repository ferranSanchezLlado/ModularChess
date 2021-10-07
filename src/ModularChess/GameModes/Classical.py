from itertools import cycle
from typing import List, Tuple, TYPE_CHECKING, cast

import numpy as np

from ModularChess.GameModes.GameMode import GameState, GameMode
from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.pieces.Bishop import Bishop
from ModularChess.pieces.King import King
from ModularChess.pieces.Knight import Knight
from ModularChess.pieces.Pawn import Pawn
from ModularChess.pieces.Queen import Queen
from ModularChess.pieces.Rook import Rook
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Position import Position
from ModularChess.utils.Promotion import Promotion

if TYPE_CHECKING:
    from ModularChess.utils.Movement import Movement


class Classical(GameMode):

    def __init__(self, white: "Player", black: "Player"):

        self.white = white
        self.black = black
        self.last_capture = 0

        players = [self.white, self.black]
        Player.join_allies([self.white], players)
        Player.join_allies([self.black], players)

        self_classical = self

        class ClassicalPawn(Pawn):
            # TODO: En passant only next turn

            def __init__(self, board: "Board", player: "Player", starting_position: Position):
                super(ClassicalPawn, self).__init__(board, player, starting_position, [Queen, Rook, Bishop, Knight])

            def can_promote_in_position(self, new_position: Position) -> bool:
                promotion_y = 7 if self.player == white else 0
                return bool(new_position[0] == promotion_y)

            def check_promotion(self, new_position: Position) -> List["Movement"]:
                if self.can_promote_in_position(new_position):
                    return [Promotion(self, new_position, piece_type) for piece_type in self.valid_pieces_type]
                return [BasicMovement(self, new_position)]

            def check_move(self, new_position: Position) -> List["Movement"]:
                # Piece didn't move or outside board
                if super(Pawn, self).check_move(new_position) is None:
                    return []

                direction_player: Position = Position([-1, 0]) if self.player == black else Position([1, 0])
                diff: Position = new_position - self.position

                # Capture

                if np.max(np.abs(diff)) == np.min(np.abs(diff)) == 1 and diff[0] == direction_player[0] and \
                        self.board.can_capture(self, new_position):
                    return self.check_promotion(new_position)

                # En Passant
                enemy_piece = self.board[self.position + Position((0, diff[1]))]
                if np.max(np.abs(diff)) == np.min(np.abs(diff)) == 1 and diff[0] == direction_player[0] and \
                        self.board.can_capture(self, self.position + Position((0, diff[1]))) and \
                        enemy_piece.n_moves == 1 and (self.player == white and self.position[0] == 4  # type: ignore
                                                      or self.player == black and self.position[0] == 3) and \
                        self_classical.moves[-1].piece == enemy_piece:
                    return [BasicMovement(self, new_position)]

                # Checks pieces in the path and that it's lineal
                try:
                    if any(self.board[pos] for pos in self.position.create_lineal_path(new_position)):
                        return []
                except Exception:
                    return []

                # Base movement
                if np.array_equal(diff, direction_player):
                    return self.check_promotion(new_position)

                # Initial movement
                if np.array_equal(diff, 2 * direction_player) and self.n_moves == 0:
                    return [BasicMovement(self, new_position)]

                return []

            def get_valid_moves(self) -> List["Movement"]:
                moves: List["Movement"] = []
                direction_player = Position([-1, 0]) if self.player == black else Position([1, 0])

                # Base movement
                move: Position = self.position + direction_player
                if self.board.is_position_inside(move) and self.board[move] is None:
                    if move[0] == (0 if self.player == black else 7):
                        for piece_type in self.valid_pieces_type:
                            moves.append(Promotion(self, move, piece_type))
                    else:
                        moves.append(BasicMovement(self, move))

                # Initial movement
                move = cast(Position, self.position + 2 * direction_player)
                if self.board.is_position_inside(move) and self.n_moves == 0 and \
                        not any(self.board[pos] for pos in self.position.create_lineal_path(move)):
                    moves.append(BasicMovement(self, move))

                for x in (Position([0, -1]), Position([0, 1])):
                    move = self.position + direction_player + x
                    # Capture
                    if self.board.is_position_inside(move) and self.board.can_capture(self, move):
                        if move[0] == (0 if self.player == black else 7):  # type: ignore
                            for piece_type in self.valid_pieces_type:
                                moves.append(Promotion(self, move, piece_type))
                        else:
                            moves.append(BasicMovement(self, move))
                    # En Passant
                    elif self.board.is_position_inside(move) and (enemy_piece := self.board[self.position + x]) is not \
                            None and self.player.can_capture(enemy_piece.player) and enemy_piece.n_moves == 1 and \
                            (self.player == white and self.position[0] == 4 or self.player == black and
                             self.position[0] == 3) and self_classical.moves[-1].piece == enemy_piece:
                        moves.append(BasicMovement(self, move))

                return moves

        pieces = [ClassicalPawn, Bishop, Knight, Rook, Queen, King]

        # for piece in pieces:
        #     piece.__prev_repr__ = piece.__repr__
        #     piece.__repr__ = lambda piece_self: chr(ord(piece_self.__prev_repr__()) +
        #                                             (6 if piece_self.player == black else 0))

        super(Classical, self).__init__(Board((8, 8)), cycle((white, black)), pieces)

    def generate_board(self) -> None:
        for pos0, pos1, color in ((0, 1, self.white), (self.board.size - 1, self.board.size - 2, self.black)):
            self.board.add_piece(self.Rook(self.board, color, Position([pos0, 0])))  # type: ignore
            self.board.add_piece(self.Rook(self.board, color, Position([pos0, 7])))  # type: ignore

            self.board.add_piece(self.Knight(self.board, color, Position([pos0, 1])))  # type: ignore
            self.board.add_piece(self.Knight(self.board, color, Position([pos0, 6])))  # type: ignore

            self.board.add_piece(self.Bishop(self.board, color, Position([pos0, 2])))  # type: ignore
            self.board.add_piece(self.Bishop(self.board, color, Position([pos0, 5])))  # type: ignore

            self.board.add_piece(self.Queen(self.board, color, Position([pos0, 3])))  # type: ignore
            self.board.add_piece(self.King(self.board, color, Position([pos0, 4])))  # type: ignore

            for i in range(self.board.size):
                self.board.add_piece(self.ClassicalPawn(self.board, color, Position([pos1, i])))  # type: ignore

    def check_game_state(self) -> Tuple["GameState", List["Player"]]:
        if np.all(self.board.board == None):  # noqa: E711
            return GameState.EMPTY, []
        if len(self.moves) == 0:
            return GameState.STARTING, []
        if self.check_checkmate():
            return GameState.CHECKMATE, [self.turn.enemies[0]]
        if self.check_stalemate():
            return GameState.STALEMATE, [self.white, self.black]
        if self.check_more_than_50_moves():
            return GameState.MOVES_50, [self.white, self.black]
        return GameState.PLAYING, []

    def check_stalemate(self) -> bool:
        king = self.board.pieces[self.turn][self.King][0]  # type: ignore
        return self.board.can_enemy_piece_capture_piece(king) is None and len(self.generate_moves()) == 0

    def check_checkmate(self) -> bool:
        king = self.board.pieces[self.turn][self.King][0]  # type: ignore
        return self.board.can_enemy_piece_capture_piece(king) is not None and len(self.generate_moves()) == 0

    def move(self, move: "Movement") -> None:
        super(Classical, self).move(move)
        if move.piece_is_captured():
            self.last_capture = len(self.moves)

    def check_more_than_50_moves(self) -> bool:
        return len(self.moves) > self.last_capture + 100

    def check_valid_move(self, move: "Movement") -> bool:
        king = self.board.pieces[move.player][self.King][0]  # type: ignore
        # Checks king is not being moved and tests for checks

        self.force_move(move)
        will_not_be_in_check = self.board.can_enemy_piece_capture_piece(king) is None
        self.undo_move(1, change_turn=False)
        return will_not_be_in_check
