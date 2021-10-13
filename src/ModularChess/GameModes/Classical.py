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
from ModularChess.utils.EnPassant import EnPassant
from ModularChess.utils.Position import Position
from ModularChess.utils.Promotion import Promotion

if TYPE_CHECKING:
    from ModularChess.utils.Movement import Movement
    from ModularChess.pieces.Piece import Piece


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

            def __init__(self, board: "Board", player: "Player", starting_position: Position):
                super().__init__(board, player, starting_position, [Queen, Rook, Bishop, Knight])
                self.direction_player: Position = Position([-1, 0]) if self.player == black else Position([1, 0])

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

                diff: Position = new_position - self.position
                abs_diff: Position = np.abs(diff)

                # Capture
                if abs_diff.max() == abs_diff.min() == 1 and diff[0] == self.direction_player[0]:

                    if self.board.can_capture(self, new_position):
                        return self.check_promotion(new_position)

                    # En Passant
                    en_passant_position: Position = self.position + Position((0, diff[1]))
                    enemy_piece = self.board[en_passant_position]
                    if enemy_piece is not None and self.player.can_capture(enemy_piece.player) and \
                            enemy_piece.n_moves == 1 and int(4.5 - self.direction_player[0] / 2) == self.position[0] \
                            and self_classical.moves[-1].piece == enemy_piece:
                        return [EnPassant(self, new_position, enemy_piece)]

                # Base movement
                if self.board[self.position + self.direction_player] is None:
                    if np.array_equal(diff, self.direction_player):
                        return self.check_promotion(new_position)

                    # Initial movement
                    if np.array_equal(diff, 2 * self.direction_player) and self.n_moves == 0 and \
                            self.board[new_position] is None:
                        return [BasicMovement(self, new_position)]

                return []

            def get_valid_moves(self) -> List["Movement"]:
                moves: List["Movement"] = []
                direction_player = Position([-1, 0]) if self.player == black else Position([1, 0])

                # Base movement
                move: Position = self.position + direction_player
                if self.board.is_position_inside(move) and self.board[move] is None:
                    moves += self.check_promotion(move)

                # Initial movement
                move = cast(Position, self.position + 2 * direction_player)
                if self.board.is_position_inside(move) and self.n_moves == 0 and \
                        not any(self.board[pos] for pos in self.position.create_lineal_path(move)):
                    moves.append(BasicMovement(self, move))

                for x in (Position([0, -1]), Position([0, 1])):
                    move = self.position + direction_player + x
                    if self.board.is_position_inside(move):
                        # Capture
                        if self.board.can_capture(self, move):
                            moves += self.check_promotion(move)
                        # En Passant
                        else:
                            enemy_piece = self.board[self.position + x]
                            if enemy_piece is not None and self.player.can_capture(enemy_piece.player) and \
                                    enemy_piece.n_moves == 1 and int(4.5 - self.direction_player[0] / 2) == \
                                    self.position[0] and self_classical.moves[-1].piece == enemy_piece:
                                moves.append(EnPassant(self, move, enemy_piece))

                return moves

        def custom_repr(piece_self: "Piece"):
            return chr(ord(piece_self.piece_unicode()) + (6 if piece_self.player == white else 0))

        pieces = [ClassicalPawn, Bishop, Knight, Rook, Queen, King]
        for piece in pieces:
            piece.__repr__ = custom_repr  # type: ignore

        super().__init__(Board((8, 8)), cycle((white, black)), pieces)

    def __del__(self):
        def original_repr(piece_self: "Piece"):
            return piece_self.piece_unicode()

        for piece in self.pieces:
            piece.__repr__ = original_repr  # type: ignore

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
            return GameState.EMPTY_BOARD, []
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
        super().move(move)
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

    def restart(self) -> None:
        self.last_capture = 0
        self.order = cycle((self.white, self.black))
        self.turn = next(self.order)
        self.board = Board((8, 8))
