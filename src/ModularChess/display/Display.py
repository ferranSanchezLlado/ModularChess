import os

import pygame

from ModularChess.GameModes.GameMode import GameMode, GameState
from ModularChess.utils.Position import Position


def color_surface(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[arr.sum(axis=-1) > 10] = red, green, blue


class Display:
    res_path = os.path.join("..", "..", "res")
    black_square = (116, 152, 174)
    white_square = (212, 224, 229)

    def __init__(self, game_mode: "GameMode", screen_width=768, screen_height=768):
        pygame.display.init()
        pygame.font.init()

        self.game_mode = game_mode
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.clock = pygame.time.Clock()
        self.chess_font = pygame.font.SysFont('calibri', 24)  # Times new Roman
        self.screen = pygame.display.set_mode([screen_width, screen_height])

        pygame.display.set_caption("Modular Chess")

        icon = pygame.image.load(open(os.path.join(self.res_path, "Icon.png")))
        pygame.display.set_icon(icon)

        self.x_size, self.y_size, self.other_size = (self.game_mode.board.shape[0], self.game_mode.board.shape[1],
                                                     self.game_mode.board.shape[2:])

        self.square_size_x = screen_width // self.x_size
        self.square_size_y = screen_height // self.y_size

        self.draw_board()

    def game_loop(self):
        while 1:
            prev_pos, piece, next_move = None, None, None
            while self.game_mode.check_game_state()[0] != GameState.FINISHED:
                self.clock.tick(5)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        coord = Position((7 - event.pos[1] // self.square_size_y, event.pos[0] // self.square_size_x))

                        print(coord)
                        if prev_pos is None:
                            prev_pos = coord
                            piece = self.game_mode.board[prev_pos]

                            if piece is None:
                                print("No piece in the clicked box")
                                prev_pos = None
                            elif piece.player != self.game_mode.turn:
                                print("It's not your turn")
                                prev_pos = None
                        else:
                            print("Move: ", prev_pos, "->", coord)  # type: ignore
                            moves = piece.check_move(coord)
                            chosen_index = None
                            if len(moves) == 0:
                                print("Invalid move")
                            elif len(moves) == 1:
                                chosen_index = 0
                            else:
                                while True:
                                    try:
                                        chosen_index = int(input("Valid moves: \n - " + '\n - '.join(
                                            str(move) for move in moves)))
                                        if 0 <= chosen_index < len(moves):
                                            break
                                    except ValueError:
                                        pass
                                    print("That's not a valid option!")
                            if chosen_index is not None:
                                try:
                                    self.game_mode.move(moves[chosen_index])
                                except Exception:
                                    print("Invalid Move")

                            self.draw_board()
                            prev_pos = None
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT and len(self.game_mode.moves) > 0:
                            next_move = self.game_mode.moves[-1]
                            self.game_mode.undo_move(1)
                        elif event.key == pygame.K_RIGHT and next_move is not None:
                            self.game_mode.move(next_move)
                            next_move = None
                        elif event.key == pygame.K_r:
                            self.game_mode.restart()
                            self.game_mode.generate_board()
                        self.draw_board()

                    pygame.display.update()

            self.game_mode.restart()
            self.game_mode.generate_board()
            self.draw_board()

    def draw_board(self):
        for y in range(self.y_size):
            for x in range(self.x_size):
                color = self.white_square if (x + y) % 2 == 0 else self.black_square
                pygame.draw.rect(self.screen, color, (x * self.square_size_x, y * self.square_size_y,
                                                      (x + 1) * self.square_size_x, (y + 1) * self.square_size_y))

                opposite_color = self.white_square if (x + y) % 2 == 1 else self.black_square
                if x == 0:  # Draws y index
                    text_surface = self.chess_font.render(str(8 - y), False, opposite_color)
                    pygame.Surface.blit(self.screen, text_surface,
                                        (x * self.square_size_x + self.square_size_x // (2 * self.x_size),
                                         y * self.square_size_y + self.square_size_y // (2 * self.y_size)))
                if y == 7:  # Draws x index
                    text_surface = self.chess_font.render(chr(ord('a') + x), False, opposite_color)
                    pygame.Surface.blit(self.screen, text_surface,
                                        ((x + 1) * self.square_size_x - self.square_size_x // (self.x_size // 2),
                                         (y + 1) * self.square_size_y - self.square_size_y // (self.y_size // 2)))

                piece = self.game_mode.board[(7 - y, x)]
                if piece is not None:
                    piece_image = pygame.image.load(piece.image())
                    picture = pygame.transform.scale(piece_image, (self.square_size_x, self.square_size_y))
                    picture.convert_alpha()
                    color_surface(picture, *piece.player.color)

                    pygame.Surface.blit(self.screen, picture, (x * self.square_size_x, y * self.square_size_y))
