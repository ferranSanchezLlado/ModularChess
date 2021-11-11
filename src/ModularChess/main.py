import datetime
import random

from guppy import hpy

from ModularChess.artificial_intelligence.BasicAI import BasicAI
from ModularChess.artificial_intelligence.BasicEvaluator import BasicEvaluator
from ModularChess.artificial_intelligence.RandomAI import RandomAI
from ModularChess.controller.Player import Player
from ModularChess.game_modes.Classical import Classical
from ModularChess.game_modes.GameMode import GameState
from display.Display import Display


def main():
    game_mode = Classical(Player("white", (255, 255, 255)), Player("black", (0, 0, 0)))
    game_mode.generate_board()
    ai = RandomAI(game_mode.black, BasicEvaluator(game_mode))
    ai2 = BasicAI(2, game_mode.white, BasicEvaluator(game_mode))
    display = Display(game_mode, [ai, ai2])
    display.game_loop()


def main_play():
    h = hpy()
    h.setrelheap()
    white, black = Player("White"), Player("Black")
    random.seed(0)
    wins = {white: 0.0, black: 0.0, "draw": 0}
    avg_time = datetime.timedelta()

    for n in range(20):
        classical = Classical(white, black)
        classical.generate_board()
        initial_time = datetime.datetime.now()

        result = classical.check_game_state()
        while result[0] != GameState.FINISHED:
            moves = classical.generate_moves()
            move = random.choice(moves)
            classical.move(move)
            result = classical.check_game_state()

        for player in result[1]:
            wins[player] += 1 / len(result[1])
        if result[0] == GameState.DRAW:
            wins['draw'] += 1
        print(result)
        print(classical.board)

        diff = datetime.datetime.now() - initial_time
        avg_time_game = (avg_time * n + diff) / (n + 1)
        avg_time_move = (avg_time * n + diff / len(classical.moves)) / (n + 1)

        print(f"--- GAME {n + 1} ---")
        print(f"SCORE\n - WHITE: {wins[white]}\n - BLACK: {wins[black]}\nNumber of Draws: {wins['draw']}")
        print("AVERAGE TIME PER GAME: " + str(avg_time_game))
        print("AVERAGE TIME PER MOVE: " + str(avg_time_move) + "\n")

    # print(h.heap())
    # print(h.heap().byid[0].sp)
    # print(h.iso(1, [], {}))


def main3():
    white, black = Player("White"), Player("Black")
    classical = Classical(white, black)
    classical.generate_board()
    print(classical.to_fen())
    ai = BasicAI(2, white, BasicEvaluator(classical))
    print(ai.score())
    print(ai.get_next_move())


if __name__ == '__main__':
    main()
    # main3()

# TODO
"""
- Game Controller
- Refactor testes
- Already checked valid movement (speed performance)
- Rich format (for better console log)
"""
