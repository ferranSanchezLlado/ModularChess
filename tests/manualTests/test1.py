from typing import Type

from ModularChess.GameModes.Classical import Classical
from ModularChess.controller.Board import Board
from ModularChess.controller.Player import Player
from ModularChess.pieces.Bishop import Bishop
from ModularChess.pieces.Empty import Empty
from ModularChess.pieces.King import King
from ModularChess.pieces.Knight import Knight
from ModularChess.pieces.Piece import Piece
from ModularChess.pieces.Queen import Queen
from ModularChess.pieces.Rook import Rook
from ModularChess.utils.Position import Position


def test1():
    game_mode = Classical(Player("White", None), Player("Black", None))
    game_mode.generate_board()

    print(game_mode.board)

    pieces: list[Type[Piece]] = [Bishop, King, Knight, Queen, Rook]

    for Piece_Cls in pieces:
        board = Board(dimensions=3)

        initial_position = Position([4, 4, 4])
        piece = Piece_Cls(board, game_mode.white, initial_position)
        board.add_piece(piece)

        print(board)

        # Set of all positions that pass the check method
        pos_set_all_combinations = set()
        for x in range(board.size):
            for i in range(board.size):
                for j in range(board.size):
                    pos: Position = Position([i, j, x])
                    if piece.check_move(pos):
                        pos_set_all_combinations.add(tuple(pos))

        print("Valid Moves (all): ", pos_set_all_combinations)

        # Check valid moves pass check move
        pos_set_valid_moves = set()
        for move in piece.get_valid_moves():
            assert move.check_valid_move()
            pos_set_valid_moves.add(tuple(move.movements[0].destination_position))

        print("Valid Moves (valid): ", pos_set_valid_moves)

        # Checks previous set and all valid moves are the same
        assert pos_set_all_combinations == pos_set_valid_moves

        # Displays possible moves by pieces
        for moves in piece.get_valid_moves():
            tmp = Empty(board, game_mode.black, moves.movements[0].destination_position)
            board.add_piece(tmp)
        print(board)


if __name__ == "__main__":
    test1()
    exit(0)
