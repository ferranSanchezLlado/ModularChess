import os
from typing import cast, Optional, List

import numpy as np
import pygame

from ModularChess.artificial_intelligence.AI import AI
from ModularChess.display.Sprites import TileSprite, PieceSprite
from ModularChess.game_modes.GameMode import GameMode, GameState
from ModularChess.movements.Movement import Movement, MovementType
from ModularChess.utils.Exceptions import InvalidMoveException
from ModularChess.utils.Position import Position


class Display:
    res_path = os.path.join("..", "..", "res")
    black_square = (116, 152, 174)
    white_square = (212, 224, 229)

    def __init__(self, game_mode: "GameMode", ai: Optional[List["AI"]] = None, screen_width=768, screen_height=768):
        pygame.display.init()
        pygame.font.init()

        self.game_mode = game_mode
        self.ai = ai if ai is not None else []
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.clock = pygame.time.Clock()
        self.chess_font = pygame.font.SysFont('calibri', 24)  # Times new Roman
        self.screen = pygame.display.set_mode([screen_width, screen_height])

        pygame.display.set_caption("Modular Chess")

        icon = pygame.image.load(open(os.path.join(self.res_path, "Icon.png")))
        pygame.display.set_icon(icon)

        self.other_size, self.y_size, self.x_size = (self.game_mode.board.shape[:2], self.game_mode.board.shape[-2],
                                                     self.game_mode.board.shape[-1])

        self.square_size_x = screen_width // self.x_size
        self.square_size_y = screen_height // self.y_size

        self.tiles = pygame.sprite.Group()
        self.pieces = pygame.sprite.Group()

        self.load_sprites()
        self.draw_board()

    def find_ai_turn(self) -> Optional["AI"]:
        for ai in self.ai:
            if ai.player == self.game_mode.current_player_turn:
                return ai
        return None

    def game_loop(self):
        while 1:
            undone_moves: List[Movement] = []
            clicked_piece_sprite: Optional[PieceSprite] = None
            original_tile: Optional[TileSprite] = None
            valid_destination_tiles: List[TileSprite] = []
            click_offset_x, click_offset_y = 0, 0

            while self.game_mode.check_game_state()[0] != GameState.FINISHED:
                ai_turn = self.find_ai_turn()
                if ai_turn is not None:
                    ai_move = ai_turn.get_next_move()
                    self.game_mode.move(ai_move)
                    self.update_move(ai_move)
                    self.draw_board()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                        mouse_x, mouse_y = event.pos
                        x, y = (mouse_x // self.square_size_x, mouse_y // self.square_size_y)

                        selected_piece = self.game_mode.board[(self.y_size - y - 1, x)]
                        if selected_piece is None:
                            print("No piece in the clicked box")
                        elif selected_piece.player != self.game_mode.current_player_turn:
                            print("It's not your turn")
                        else:
                            clicked_pieces = [s for s in self.pieces if
                                              cast(PieceSprite, s).rect.collidepoint((mouse_x, mouse_y))]
                            assert len(clicked_pieces) == 1
                            clicked_piece_sprite = cast(PieceSprite, clicked_pieces[0])
                            click_offset_x = clicked_piece_sprite.rect.x - mouse_x
                            click_offset_y = clicked_piece_sprite.rect.y - mouse_y

                            tile_sprites_list = self.tiles.sprites()
                            original_tile = cast(TileSprite, tile_sprites_list[y * self.y_size + x])
                            original_tile.change_color((151, 218, 234))

                            move_positions = (move.destination for move in
                                              self.game_mode.generate_moves_of_a_piece(selected_piece))
                            valid_destination_tiles = [cast(TileSprite, tile_sprites_list[(self.y_size - 1 - pos[0]) *
                                                                                          self.y_size + pos[1]])
                                                       for pos in move_positions]
                            for tile in valid_destination_tiles:
                                tile.add_small_circle((255, 0, 0))

                    elif event.type == pygame.MOUSEMOTION:
                        if clicked_piece_sprite is not None:
                            mouse_x, mouse_y = event.pos
                            clicked_piece_sprite.rect.x = mouse_x + click_offset_x
                            clicked_piece_sprite.rect.y = mouse_y + click_offset_y
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                        if clicked_piece_sprite is not None:
                            mouse_x, mouse_y = event.pos
                            x, y = (mouse_x // self.square_size_x, mouse_y // self.square_size_y)
                            coord = Position((self.y_size - y - 1, x))

                            moves = clicked_piece_sprite.piece.check_piece_valid_move(coord)
                            chosen_index = None
                            if len(moves) == 0:
                                clicked_piece_sprite.update_with_piece_position()
                                print("Invalid move")
                            elif len(moves) == 1:
                                chosen_index = 0
                            else:
                                str_move = ("Valid moves: \n " + '\n '.join(f'{i}: {move}'
                                                                            for i, move in enumerate(moves))) + "\n"

                                while True:
                                    try:
                                        chosen_index = int(input(str_move))
                                        if 0 <= chosen_index < len(moves):
                                            break
                                    except ValueError:
                                        pass
                                    print("That's not a valid option!")
                            if chosen_index is not None:
                                try:
                                    self.game_mode.move(moves[chosen_index])
                                    self.update_move(moves[chosen_index])
                                    undone_moves = []
                                except InvalidMoveException:
                                    clicked_piece_sprite.update_with_piece_position()
                                    print("Invalid Move")
                        clicked_piece_sprite = None
                        if original_tile is not None:
                            original_tile.reset()
                            for tile in valid_destination_tiles:
                                tile.reset()
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT and len(self.game_mode.moves) > 0:
                            undone_moves.append(self.game_mode.moves[-1])
                            self.game_mode.undo_move(1)
                            self.update_move(undone_moves[-1].inverse())
                        elif event.key == pygame.K_RIGHT and len(undone_moves) > 0:
                            ai_move = undone_moves.pop()
                            self.game_mode.move(ai_move)
                            self.update_move(ai_move)
                        elif event.key == pygame.K_r:
                            self.restart_game()
                    self.draw_board()

            self.restart_game()
            self.draw_board()

    def restart_game(self):
        self.game_mode.restart()
        self.game_mode.generate_board()
        self.load_sprites()

    def load_sprites(self):
        self.tiles = pygame.sprite.Group()
        self.pieces = pygame.sprite.Group()
        for y in range(self.y_size):
            for x in range(self.x_size):

                self.tiles.add(TileSprite(x, y, self.square_size_x, self.square_size_y, self.white_square,
                                          self.black_square, self.chess_font))

                piece = self.game_mode.board[(7 - y, x)]
                if piece is not None:
                    self.pieces.add(PieceSprite(x, y, self.square_size_x, self.square_size_y, piece))

    def draw_board(self):
        self.tiles.draw(self.screen)
        self.pieces.draw(self.screen)
        pygame.display.update()

    def update_move(self, move: Movement):
        for move_data in move.movements:
            move_type = move_data.type
            if move_type == MovementType.ADDITION:
                assert move_data.destination_position is not None
                x, y = move_data.destination_position[1], 7 - move_data.destination_position[0]
                self.pieces.add(PieceSprite(x, y, self.square_size_x, self.square_size_y, move_data.piece))
            elif move_type == MovementType.REMOVAL:
                piece_sprite = [piece for piece in self.pieces if move_data.piece is cast(PieceSprite, piece).piece and
                                np.array_equal(cast(PieceSprite, piece).piece.position,
                                               cast(Position, move_data.initial_position))][0]
                self.pieces.remove(piece_sprite)
            else:
                assert move_data.destination_position is not None
                piece_sprite = [cast(PieceSprite, piece) for piece in self.pieces if move_data.piece is
                                cast(PieceSprite, piece).piece and
                                np.array_equal(cast(PieceSprite, piece).piece.position,
                                               move_data.destination_position)][0]
                x, y = move_data.destination_position[1], 7 - move_data.destination_position[0]
                piece_sprite.rect.x, piece_sprite.rect.y = x * piece_sprite.rect.width, y * piece_sprite.rect.height
