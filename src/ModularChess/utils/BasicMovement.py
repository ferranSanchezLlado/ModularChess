from src.ModularChess.pieces.Piece import Piece
from src.ModularChess.utils.Movement import Movement, MovementData
from src.ModularChess.utils.Position import Position


class BasicMovement(Movement):

    def __init__(self, piece: Piece, new_position: Position):
        move = [MovementData(piece, piece.position, new_position)]
        # Adds information about capture
        if piece.board.is_there_an_enemy_piece(piece, new_position):
            enemy_piece = piece.board[new_position]
            assert enemy_piece is not None
            move += [MovementData(enemy_piece, new_position, None)]
        super().__init__(move)

    def check_valid_move(self) -> bool:
        return super().check_valid_move()
