from enum import Enum

import pygame

from conts import TILE_SIZE


class TILE_TYPES(Enum):
    NONE = 0
    PATH = 1
    START_POINT = 2
    END_POINT = 3
    LIFT = 4


tile_path_map = {
    TILE_TYPES.NONE: "./assets/tiles/tile.png",
    TILE_TYPES.PATH: "./assets/tiles/empty.png",
    TILE_TYPES.START_POINT: "./assets/tiles/empty.png",
    TILE_TYPES.END_POINT: "./assets/tiles/empty.png",
    TILE_TYPES.LIFT: "./assets/tiles/empty.png",
}


class Lift(pygame.sprite.Sprite):
    def __init__(self, pos):

        self.image = pygame.image.load("./assets/tiles/lift.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = pygame.Rect(*pos, TILE_SIZE, TILE_SIZE)
        self.x, self.y = pos
        self.moveing = False

    @property
    def tile_pos(self):
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)

    @property
    def pos(self):
        return self.x, self.y

    def update_rect(self):
        self.rect = pygame.Rect((self.x, self.y, TILE_SIZE, TILE_SIZE))

    def update(self, players):
        if self.moveing:
            self.x, self.y = self.next_pos.pop(0)
            self.update_rect()


class Tile(pygame.sprite.Sprite):
    """
    Tile represents a level tile not in path
    """

    def __init__(self, tile, pos):
        super().__init__()
        if tile in tile_path_map:
            self.image = pygame.image.load(tile_path_map[tile])
        else:
            self.image = pygame.image.load("./assets/fail.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = pygame.Rect(*pos, TILE_SIZE, TILE_SIZE)


class Level:
    def __init__(self, path):
        from level_loader import get_level, parse_level_data

        self.level_data = get_level(path)
        self.level, self.path = parse_level_data(self.level_data)
        self.start_point = (
            self.path[0][1] * TILE_SIZE,
            self.path[0][0] * TILE_SIZE,
        )
        self.tiles = pygame.sprite.Group()
        self.create_tiles()

    def create_tiles(self):
        for i, row in enumerate(self.level):
            for j, tile in enumerate(row):
                self.tiles.add(Tile(tile, (j * TILE_SIZE, i * TILE_SIZE)))

    @property
    def num_board(self):
        return [[j.value for j in i] for i in self.level]

    def draw(self, win):
        self.tiles.draw(win)
