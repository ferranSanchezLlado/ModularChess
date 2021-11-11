from typing import Tuple, Optional, cast

import pygame

from ModularChess.pieces.Piece import Piece


def color_surface(surface: pygame.surface.Surface, color: Tuple[int, int, int]):
    arr = pygame.surfarray.pixels3d(surface)
    arr[arr.sum(axis=-1) > 128] = color


class TileSprite(pygame.sprite.DirtySprite):

    def create_image(self, color: Tuple[int, int, int], opposite_color: Optional[Tuple[int, int, int]] = None):
        inv_color: Tuple[int, int, int] = opposite_color or cast(Tuple[int, int, int], tuple(255 - el for el in color))
        self.image: pygame.surface.Surface = pygame.Surface([self.width, self.height])
        self.image.fill(color)

        if self.x_index == 0:
            text_surface = self.font.render(str(8 - self.y_index), False, inv_color)
            self.image.blit(text_surface, (self.width // 32, self.height // 32))
        if self.y_index == 7:
            text_surface = self.font.render(chr(ord('a') + self.x_index), False, inv_color)
            text_rect = text_surface.get_rect()
            self.image.blit(text_surface, (self.width - text_rect.width - self.width // 32,
                                           self.height - text_rect.height - self.height // 32))

        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x_index * self.width, self.y_index * self.height

    def __init__(self, x_index: int, y_index: int, width: int, height: int, white_square: Tuple[int, int, int],
                 black_square: Tuple[int, int, int], font: pygame.font.Font):
        super().__init__()

        self.width = width
        self.height = height
        self.font = font
        self.x_index = x_index
        self.y_index = y_index

        self.color = white_square if (x_index + y_index) % 2 == 0 else black_square
        self.opposite_color = white_square if (x_index + y_index) % 2 == 1 else black_square

        self.create_image(self.color, self.opposite_color)

    def change_color(self, new_color: Tuple[int, int, int]):
        self.create_image(new_color)

    def reset(self):
        self.create_image(self.color, self.opposite_color)

    def add_small_circle(self, color: Tuple[int, int, int]):
        pygame.draw.circle(self.image, color, (self.rect.width // 2, self.rect.height // 2),
                           self.rect.width // 10)


class PieceSprite(pygame.sprite.DirtySprite):

    def __init__(self, x_index: int, y_index: int, width: int, height: int, piece: Piece):
        super().__init__()

        self.piece = piece
        self.image: pygame.surface.Surface = pygame.transform.scale(pygame.image.load(piece.image()), (width, height))
        self.image.convert_alpha()
        color_surface(self.image, piece.player.color)

        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_index * width, y_index * height

    def update_with_piece_position(self):
        position = self.piece.position
        self.rect.x, self.rect.y = position[1] * self.rect.width, (7 - position[0]) * self.rect.height
