import datetime
import random

import pygame as pygame

from ModularChess.GameModes.Classical import Classical
from ModularChess.GameModes.GameMode import GameState
from ModularChess.controller.Player import Player
from display.Display import Display


def color_surface(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[arr.sum(axis=-1) > 10] = red, green, blue


def main():
    game_mode = Classical(Player("white", (255, 255, 255)), Player("black", (0, 0, 0)))
    game_mode.generate_board()
    display = Display(game_mode)
    display.game_loop()


def main_play():
    white, black = Player("White"), Player("Black")
    random.seed(0)
    wins = {white: 0.0, black: 0.0, "draw": 0}
    avg_time = datetime.timedelta()
    n = 0

    while n < 100:
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

        n += 1
        diff = (datetime.datetime.now() - initial_time)
        avg_time_game = (avg_time * n + diff) / (n + 1)
        avg_time_move = (avg_time * n + diff / len(classical.moves)) / (n + 1)

        print(f"--- GAME {n} ---")
        print(f"SCORE\n - WHITE: {wins[white]}\n - BLACK: {wins[black]}\nNumber of Draws: {wins['draw']}")
        print("AVERAGE TIME PER GAME: " + str(avg_time_game))
        print("AVERAGE TIME PER MOVE: " + str(avg_time_move) + "\n")

    # classical = Classical(white, black)
    # classical.generate_board()
    #
    # classical.move(classical.board[Position("g1")].check_move(Position("f3"))[0])
    # classical.move(classical.board[Position("e7")].check_move(Position("e5"))[0])
    #
    # classical.move(classical.board[Position("d2")].check_move(Position("d3"))[0])
    # classical.move(classical.board[Position("d8")].check_move(Position("h4"))[0])
    #
    # classical.move(classical.board[Position("b1")].check_move(Position("d2"))[0])
    # print(classical.board)
    # print([str(move) for move in classical.moves])
    #
    # print(classical.generate_moves())
    # assert GameState.FINISHED, black == classical.check_game_state()


if __name__ == '__main__':
    main()

# TODO
"""
- Game Controller
- Automatic Testing (game mode)
- Coverage
- Documentation
- Custom Exceptions
- Refactor testes
"""
