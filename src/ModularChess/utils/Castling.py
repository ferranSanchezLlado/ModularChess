import numpy as np

from src.ModularChess.pieces.King import King
from src.ModularChess.pieces.Rook import Rook
from src.ModularChess.utils.Movement import Movement, MovementData
from src.ModularChess.utils.Position import Position


class Castling(Movement):

    def __init__(self, king: King, position: Position):
        rooks = king.board.pieces[king.player][Rook]

        direction: Position = position - king.position

        # Checks if direction is only in one axis
        if np.sum(direction != 0) != 1:
            raise Exception("Invalid Move")
        dir_rooks = np.abs([np.sum(rook.position - position) for rook in rooks])
        rook = rooks[np.argmin(dir_rooks)]

        if rook.position[~(direction != 0)] != king.position[~(direction != 0)]:
            raise Exception("Invalid Axis")

        if rook.n_moves or king.n_moves:
            raise Exception("King or Rook has already moved once")

        # Checks pieces in the path
        if any(list(king.board[pos] for pos in king.position.create_lineal_path(rook.position))[:-1]):
            raise Exception("Piece in path")

        king_pos = king.position.copy_and_replace(direction != 0,
                                                  (3 if direction.sum() > 0 else 1) * king.board.size // 4)
        rook_pos = king_pos + (-(direction != 0).astype(np.int_) if direction.sum() > 0 else (direction != 0))

        # Checks during the path of the king
        if any(king.board.can_enemy_capture(pos, king.player.get_allies()) for pos in
               king.position.create_lineal_path(king_pos)):
            raise Exception("King would be in check during path")

        move = [MovementData(king, king.position, king_pos), MovementData(rook, rook.position, rook_pos)]
        super().__init__(move)

    def check_valid_move(self) -> bool:
        # Always true as it's checked on constructor
        return True
