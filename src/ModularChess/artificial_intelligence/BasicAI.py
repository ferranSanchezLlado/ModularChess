from typing import TYPE_CHECKING, Callable, Iterable, Tuple, List, Optional

from ModularChess.artificial_intelligence.AI import AI
from ModularChess.movements.Promotion import Promotion

if TYPE_CHECKING:
    from ModularChess.artificial_intelligence.Evaluator import Evaluator
    from ModularChess.movements.Movement import Movement
    from ModularChess.controller.Player import Player


def sort_moves(moves: Iterable['Movement']) -> Iterable['Movement']:
    sorted_moves: List[Tuple[float, "Movement"]] = []
    for move in moves:
        move_score = 0.0

        # Prioritizes the move captures the most valuable piece with the least valuable piece
        if move.piece_is_captured():
            move_score += 10.0 * sum(piece.piece_value() for piece in move.captured_pieces()) - move.piece.piece_value()

        # Prioritizes promotion moves
        if isinstance(move, Promotion):
            move_score += 10.0 * move.promoted_piece.piece_value()

        # Prioritizes castling moves

        # Penalize moves where enemy piece can capture

        # Prioritize checks

        sorted_moves.append((move_score, move))

    return iter(move for _, move in sorted(sorted_moves, key=lambda x: x[0], reverse=True))


class BasicAI(AI):

    def __init__(self, max_depth: int, player: "Player", evaluator: "Evaluator"):
        self.max_depth = max_depth
        super().__init__(player, evaluator)

    def decide_alpha_beta_path(self, move: "Movement") -> Callable[[float, float, int],
                                                                   Tuple[Optional["Movement"], float]]:
        self.evaluator.game_mode.move(move)
        next_turn_player = self.evaluator.game_mode.current_player_turn
        if next_turn_player in self.player.allies:
            return self.alpha_beta_max
        elif next_turn_player in self.player.enemies:
            return self.alpha_beta_min
        raise Exception("Movement of piece which is not an ally nor an enemy")

    def alpha_beta_max(self, alpha: float, beta: float, depth_left: int) -> Tuple[Optional["Movement"], float]:
        if depth_left == 0:
            return None, self.evaluator.score(self.player)

        best_move: Optional["Movement"] = None
        for move in sort_moves(self.evaluator.game_mode.generate_moves()):
            score = self.decide_alpha_beta_path(move)(alpha, beta, depth_left - 1)[1]
            self.evaluator.game_mode.undo_move(1)
            if score >= beta:
                return None, beta  # pruning
            if score > alpha:
                alpha = score
                best_move = move
        return best_move, alpha

    def alpha_beta_min(self, alpha: float, beta: float, depth_left: int) -> Tuple[Optional["Movement"], float]:
        if depth_left == 0:
            return None, self.evaluator.score(self.player)

        best_move: Optional["Movement"] = None
        for move in sort_moves(self.evaluator.game_mode.generate_moves()):
            score = self.decide_alpha_beta_path(move)(alpha, beta, depth_left - 1)[1]
            self.evaluator.game_mode.undo_move(1)
            if score <= alpha:
                return None, alpha  # pruning
            if score < beta:
                beta = score
                best_move = move
        return best_move, beta

    def score(self) -> float:
        return self.alpha_beta_max(float('-inf'), float('inf'), self.max_depth)[1]

    def get_next_move(self) -> "Movement":
        tmp = self.alpha_beta_max(float('-inf'), float('inf'), self.max_depth)
        if tmp[0] is None:
            tmp = self.alpha_beta_max(float('-inf'), float('inf'), self.max_depth)
            raise Exception("No moves available")
        return tmp[0]
