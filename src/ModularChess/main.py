from typing import cast

from src.ModularChess.pieces.Piece import Piece
from src.ModularChess.GameModes.Classical import Classical
from src.ModularChess.controller.Player import Player
from src.ModularChess.pieces.King import King
from src.ModularChess.pieces.Rook import Rook
from src.ModularChess.utils.BasicMovement import BasicMovement
from src.ModularChess.utils.Castling import Castling
from src.ModularChess.utils.Position import Position


def main():
    game_mode = Classical(Player("White"), Player("Black"))
    game_mode.generate_board()

    king = cast(King, game_mode.board.pieces[game_mode.white][King][0])

    try:
        Castling(king, Position("f1"))
        assert False
    except AssertionError:
        assert False
    except Exception as e:
        assert e

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
    move = Castling(king, Position("b1"))
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
    main()
    exit(0)

# TODO
"""
- Game Controller
- Display game (Interface)
- Automatic Testing
- Special Movements Pieces
- Documentation
- Custom Exceptions
"""
