from typing import cast

from ModularChess.GameModes.Classical import Classical
from ModularChess.controller.Player import Player
from ModularChess.pieces.King import King
from ModularChess.pieces.Piece import Piece
from ModularChess.pieces.Rook import Rook
from ModularChess.utils.BasicMovement import BasicMovement
from ModularChess.utils.Castling import Castling
from ModularChess.utils.Position import Position


def test3():
    game_mode = Classical(Player("White"), Player("Black"))
    game_mode.generate_board()

    king = cast(King, game_mode.board.pieces[game_mode.white][King][0])

    move = Castling(king, king.find_nearest_piece(Position("f1")))
    assert not move.check_valid_move()

    pieces = game_mode.board.pieces[game_mode.white].copy()
    pieces.pop(King)
    pieces.pop(Rook)

    for same_piece_list in pieces.values():
        same_piece_list = same_piece_list.copy()
        for piece in same_piece_list:
            print(piece.position)
            game_mode.board.remove_piece(piece)

    print(game_mode.board)
    king = cast(King, game_mode.board.pieces[game_mode.white][King][0])
    move = Castling(king, king.find_nearest_piece(Position("b1")))
    assert move.check_valid_move()
    game_mode.move(move)

    piece_to_move = cast(Piece, game_mode.board[Position("g8")])
    move2 = BasicMovement(piece_to_move, Position("f6"))
    game_mode.move(move2)
    game_mode.undo_move(2)
    game_mode.move(move)
    game_mode.move(move2)

    # move = Castling(king, Position("f1"))

    print(game_mode.board)


if __name__ == "__main__":
    test3()
    exit(0)
