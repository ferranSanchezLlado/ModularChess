from itertools import cycle
from typing import Optional, List, Tuple

import numpy as np

from src.ModularChess.GameModes.GameMode import GameState, GameMode
from src.ModularChess.controller.Board import Board
from src.ModularChess.controller.Player import Player
from src.ModularChess.pieces.Bishop import Bishop
from src.ModularChess.pieces.King import King
from src.ModularChess.pieces.Knight import Knight
from src.ModularChess.pieces.Pawn import Pawn
from src.ModularChess.pieces.Queen import Queen
from src.ModularChess.pieces.Rook import Rook
from src.ModularChess.utils.BasicMovement import BasicMovement
from src.ModularChess.utils.Movement import Movement
from src.ModularChess.utils.Position import Position


class Classical(GameMode):

    def __init__(self, white: Player, black: Player):
        super(Classical, self).__init__(Board(), cycle((white, black)))

        self.white = white
        self.black = black

        class ClassicalPawn(Pawn):

            def check_move(self, new_position: Position) -> bool:
                # Piece didn't move or outside board
                if not super(Pawn, self).check_move(new_position):
                    return False

                direction_player: Position = Position([-1, 0]) if self.player == black else Position([1, 0])
                diff: Position = new_position - self.position

                destination_piece = self.board[new_position]
                # Capture
                if np.max(np.abs(diff)) == 1 and np.min(np.abs(diff)) == 1 and diff[0] == direction_player[0] and \
                        destination_piece is not None and self.player.can_capture(destination_piece.player):
                    return True

                # En Passant
                enemy_piece = self.board[self.position + Position((0, diff[1]))]
                if np.max(np.abs(diff)) == 1 and np.min(np.abs(diff)) == 1 and diff[0] == direction_player[0] and \
                        enemy_piece is not None and enemy_piece.player != self.player and enemy_piece.n_moves == 1 and \
                        (self.player == white and self.position[0] == self.board.size - 4 or self.player == black and
                         self.position[0] == 3):
                    return True

                # Checks pieces in the path and that it's lineal
                try:
                    if any(list(self.board[pos] for pos in self.position.create_lineal_path(new_position))):
                        return False
                except Exception:
                    return False

                # Base movement
                if np.array_equal(diff, direction_player):
                    return True

                # Initial movement
                if np.array_equal(diff, 2 * direction_player) and self.n_moves == 0:
                    return True

                # TODO: Promotion
                return False

            def get_valid_moves(self) -> List[Movement]:
                moves: List[Movement] = []
                direction_player = Position([-1, 0]) if self.player == black else Position([1, 0])

                # Base movement
                move: Position = self.position + direction_player
                if self.board.is_position_inside(move) and self.board[move] is None:
                    moves.append(BasicMovement(self, move))

                # Initial movement
                move = self.position + 2 * direction_player
                if self.board.is_position_inside(move) and self.board[move] is None:
                    moves.append(BasicMovement(self, move))

                for x in (Position([0, -1]), Position([0, 1])):
                    move = self.position + direction_player + x
                    destination_piece = self.board[self.position + x]
                    # Capture
                    if self.board.is_position_inside(move) and self.board.can_capture_or_move(self, move):
                        moves.append(BasicMovement(self, move))
                    # En Passant
                    elif self.board.is_position_inside(move) and destination_piece is not None and \
                            self.player.can_capture(destination_piece.player) and destination_piece.n_moves == 1 and \
                            (self.player == white and self.position[0] == self.board.size - 4 or self.player == black
                             and self.position[0] == 3):
                        moves.append(BasicMovement(self, move))

                # TODO: Promotion

                return moves

        self.Pawn = ClassicalPawn

    def generate_board(self) -> None:
        for pos0, pos1, color in ((0, 1, self.white), (self.board.size - 1, self.board.size - 2, self.black)):
            self.board.add_piece(Rook(self.board, color, Position([pos0, 0])))
            self.board.add_piece(Rook(self.board, color, Position([pos0, 7])))

            self.board.add_piece(Knight(self.board, color, Position([pos0, 1])))
            self.board.add_piece(Knight(self.board, color, Position([pos0, 6])))

            self.board.add_piece(Bishop(self.board, color, Position([pos0, 2])))
            self.board.add_piece(Bishop(self.board, color, Position([pos0, 5])))

            self.board.add_piece(Queen(self.board, color, Position([pos0, 3])))
            self.board.add_piece(King(self.board, color, Position([pos0, 4])))

            for i in range(self.board.size):
                self.board.add_piece(self.Pawn(self.board, color, Position([pos1, i])))

    def check_game_state(self) -> Tuple[GameState, Optional[Player]]:
        return GameState.STARTING, None

    def check_valid_move(self, move: Movement) -> bool:
        king = self.board.pieces[move.player][King][0]
        # Checks king is not being moved and tests for checks
        pieces = [move.piece for move in move.movements]
        if king not in pieces:
            self.force_move(move)
            if self.board.can_enemy_capture(king.position, king.player.get_allies()):
                return False
            self.undo_move(move, change_turn=False)
        # Checks if king move would end up on check
        else:
            index = pieces.index(king)
            king_destination = move[index].destination_position
            assert king_destination is not None
            if self.board.can_enemy_capture(king_destination, king.player.get_allies()):
                return False

        return True
