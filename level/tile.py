import logging
from enum import Enum

import pygame

from conts import HEIGHT, TILE_SIZE, WIDTH
from paths import TILE_PATH_MAP
import numpy as np


class TILE_TYPES(Enum):
    NONE = 0
    PATH = 1
    START_POINT = 2
    END_POINT = 3
    LIFT = 4


class Tile(pygame.sprite.Sprite):
    """
    Tile represents a level tile not in path
    """

    def __init__(self, tile_type, pos, neighbours, coner_neighbours):
        self.image = get_tile_image(tile_type, neighbours, coner_neighbours)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        super().__init__()
        self.rect = pygame.Rect(*pos, TILE_SIZE, TILE_SIZE)
        self.pos = pos

    @property
    def corners(self):
        return (
            self.rect.topleft,
            self.rect.topright,
            self.rect.bottomright,
            self.rect.bottomleft,
        )

    @property
    def tile_corners(self):
        center = np.array(self.rect.center)

        c = [
            ((np.array(i) - center) * (0.90625 + 3 / 32)) + center for i in self.corners
        ]
        return c


pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT))

corner = pygame.image.load("./assets/tiles/empty_001.png").convert_alpha()
edge = pygame.image.load("./assets/tiles/empty_002.png").convert_alpha()
nub = pygame.image.load("./assets/tiles/empty_003.png").convert_alpha()
corner = pygame.transform.scale(corner, (TILE_SIZE, TILE_SIZE))
edge = pygame.transform.scale(edge, (TILE_SIZE, TILE_SIZE))
nub = pygame.transform.scale(nub, (TILE_SIZE, TILE_SIZE))


def add_nubs(image, neighbours):
    for i in range(-1, len(neighbours) - 1):
        if neighbours[i] and neighbours[i + 1]:
            _nub = pygame.transform.rotate(nub, 90 + i * 90)
            image.blit(_nub, (0, 0))

    return image


def add_borders(image, neighbours):
    for index, i in enumerate(neighbours):
        if not i:
            continue
        _edge = pygame.transform.rotate(edge, index * 90)
        image.blit(_edge, (0, 0))
    return image


def add_corners(image, neighbours, coner_neighbours):
    n_indexs = [n_index for n_index in range(-1, len(neighbours) - 1)]

    corners = [(index, i) for index, i in enumerate(coner_neighbours)]
    for (index, i), n_index in zip(corners, n_indexs):
        if not i:
            continue
        if neighbours[n_index] or neighbours[n_index + 1]:
            continue

        _corner = pygame.transform.rotate(corner, index * 90)
        image.blit(_corner, (0, 0))

    return image


def get_tile_image(tile_type, neighbours, coner_neighbours):

    if tile_type != TILE_TYPES.NONE:
        image = pygame.image.load("./assets/tiles/empty_000.png")
        image = add_borders(image, neighbours)
        image = add_corners(image, neighbours, coner_neighbours)
        image = add_nubs(image, neighbours)

    elif str(tile_type) in TILE_PATH_MAP:
        image = pygame.image.load(TILE_PATH_MAP[str(tile_type)])
    else:
        logging.warning(f"tile of type {tile_type} failed to load image")
        image = pygame.image.load("./assets/fail.png")

    return image
